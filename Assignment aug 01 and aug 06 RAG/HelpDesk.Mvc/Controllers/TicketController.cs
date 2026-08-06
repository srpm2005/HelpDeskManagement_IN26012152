using HelpDesk.Mvc.Models;
using HelpDesk.Mvc.Services;
using Microsoft.AspNetCore.Mvc;

namespace HelpDesk.Mvc.Controllers
{
    public class TicketController : Controller
    {
        private readonly TicketService _ticketService;

        public TicketController(TicketService ticketService)
        {
            _ticketService = ticketService;
        }

        // GET: /Ticket/Dashboard
        public async Task<IActionResult> Dashboard()
        {
            var allTickets = await _ticketService.GetAllTicketsAsync();
            var model = new DashboardViewModel
            {
                TotalTickets = allTickets.Count,
                OpenTickets = allTickets.Count(t => string.Equals(t.Status, "Open", StringComparison.OrdinalIgnoreCase)),
                ClosedTickets = allTickets.Count(t => string.Equals(t.Status, "Closed", StringComparison.OrdinalIgnoreCase)),
                RecentTickets = allTickets.OrderByDescending(t => t.CreatedDate).Take(5).ToList()
            };

            return View(model);
        }

        // GET: /Ticket or /Ticket/Index
        public async Task<IActionResult> Index(string? status)
        {
            List<Ticket> tickets;
            if (!string.IsNullOrEmpty(status) && status != "All")
            {
                tickets = await _ticketService.GetTicketsByStatusAsync(status);
                ViewBag.SelectedStatus = status;
            }
            else
            {
                tickets = await _ticketService.GetAllTicketsAsync();
                ViewBag.SelectedStatus = "All";
            }

            return View(tickets);
        }

        // GET: /Ticket/Details/5
        public async Task<IActionResult> Details(int id)
        {
            var ticket = await _ticketService.GetTicketByIdAsync(id);
            if (ticket == null)
            {
                return NotFound();
            }
            return View(ticket);
        }

        // GET: /Ticket/Create
        public IActionResult Create()
        {
            var ticket = new Ticket
            {
                Status = "Open" // Status is hardcoded to Open as per requirement
            };
            return View(ticket);
        }

        // POST: /Ticket/Create
        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> Create(Ticket ticket)
        {
            // Enforce status to Open
            ticket.Status = "Open";

            if (ModelState.IsValid)
            {
                var success = await _ticketService.CreateTicketAsync(ticket);
                if (success)
                {
                    TempData["SuccessMessage"] = "Ticket raised successfully!";
                    return RedirectToAction(nameof(Index));
                }
                ModelState.AddModelError("", "Unable to create ticket. Please check Web API connection.");
            }
            return View(ticket);
        }

        // GET: /Ticket/Edit/5
        public async Task<IActionResult> Edit(int id)
        {
            var ticket = await _ticketService.GetTicketByIdAsync(id);
            if (ticket == null)
            {
                return NotFound();
            }
            return View(ticket);
        }

        // POST: /Ticket/Edit/5
        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> Edit(int id, Ticket ticket)
        {
            if (id != ticket.Id)
            {
                return BadRequest();
            }

            if (ModelState.IsValid)
            {
                var success = await _ticketService.UpdateTicketAsync(ticket);
                if (success)
                {
                    TempData["SuccessMessage"] = "Ticket updated successfully!";
                    return RedirectToAction(nameof(Index));
                }
                ModelState.AddModelError("", "Unable to update ticket. Please check Web API connection.");
            }
            return View(ticket);
        }

        // GET: /Ticket/Delete/5
        public async Task<IActionResult> Delete(int id)
        {
            var ticket = await _ticketService.GetTicketByIdAsync(id);
            if (ticket == null)
            {
                return NotFound();
            }
            return View(ticket);
        }

        // POST: /Ticket/DeleteConfirmed/5
        [HttpPost, ActionName("DeleteConfirmed")]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> DeleteConfirmed(int id)
        {
            var success = await _ticketService.DeleteTicketAsync(id);
            if (success)
            {
                TempData["SuccessMessage"] = "Ticket deleted successfully!";
            }
            else
            {
                TempData["ErrorMessage"] = "Failed to delete ticket.";
            }
            return RedirectToAction(nameof(Index));
        }

        // GET: /Ticket/KnowledgeAssistant
        public IActionResult KnowledgeAssistant()
        {
            return View();
        }

        // POST: /Ticket/QueryKnowledgeAssistant
        [HttpPost]
        public IActionResult QueryKnowledgeAssistant([FromBody] KnowledgeQueryRequest request)
        {
            if (string.IsNullOrWhiteSpace(request?.Query))
            {
                return BadRequest(new { error = "Query cannot be empty." });
            }

            try
            {
                var rootPath = Path.GetFullPath(Path.Combine(Directory.GetCurrentDirectory(), ".."));
                var scriptPath = Path.Combine(rootPath, "cli.py");

                var psi = new System.Diagnostics.ProcessStartInfo
                {
                    FileName = "python",
                    Arguments = $"\"{scriptPath}\" --json \"{request.Query.Replace("\"", "\\\"")}\"",
                    RedirectStandardOutput = true,
                    RedirectStandardError = true,
                    UseShellExecute = false,
                    CreateNoWindow = true,
                    WorkingDirectory = rootPath,
                    StandardOutputEncoding = System.Text.Encoding.UTF8
                };

                using var process = System.Diagnostics.Process.Start(psi);
                if (process == null)
                {
                    return StatusCode(500, new { error = "Failed to launch RAG process." });
                }

                string output = process.StandardOutput.ReadToEnd();
                string error = process.StandardError.ReadToEnd();
                process.WaitForExit(5000);

                // Find valid JSON start in output
                int jsonStart = output.IndexOf('{');
                if (jsonStart >= 0)
                {
                    string jsonContent = output.Substring(jsonStart);
                    return Content(jsonContent, "application/json");
                }

                return StatusCode(500, new { error = "Failed to parse RAG response.", details = error });
            }
            catch (Exception ex)
            {
                return StatusCode(500, new { error = ex.Message });
            }
        }
    }
}


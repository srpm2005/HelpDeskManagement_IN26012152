using HelpDesk.Api.Models;
using HelpDesk.Api.Repositories;
using Microsoft.AspNetCore.Mvc;

namespace HelpDesk.Api.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class TicketController : ControllerBase
    {
        private readonly ITicketRepository _repository;

        public TicketController(ITicketRepository repository)
        {
            _repository = repository;
        }

        // GET: /api/Ticket/All
        [HttpGet("All")]
        public async Task<IActionResult> GetAllTickets()
        {
            var tickets = await _repository.GetAllTicketsAsync();
            return Ok(tickets);
        }

        // GET: /api/Ticket/{id}
        [HttpGet("{id:int}")]
        public async Task<IActionResult> GetTicketById(int id)
        {
            var ticket = await _repository.GetTicketByIdAsync(id);
            if (ticket == null)
            {
                return NotFound(new { message = $"Ticket with ID {id} not found." });
            }
            return Ok(ticket);
        }

        // POST: /api/Ticket
        [HttpPost]
        public async Task<IActionResult> CreateTicket([FromBody] Ticket? ticket)
        {
            if (ticket == null)
            {
                return BadRequest("Ticket object cannot be null.");
            }

            if (!ModelState.IsValid)
            {
                return BadRequest(ModelState);
            }

            var createdId = await _repository.CreateTicketAsync(ticket);
            return Ok(createdId);
        }

        // PUT: /api/Ticket/{id}
        [HttpPut("{id:int}")]
        public async Task<IActionResult> UpdateTicket(int id, [FromBody] Ticket ticket)
        {
            if (ticket == null || id != ticket.Id)
            {
                return BadRequest("Invalid ticket data or ID mismatch.");
            }

            var existingTicket = await _repository.GetTicketByIdAsync(id);
            if (existingTicket == null)
            {
                return NotFound(new { message = $"Ticket with ID {id} not found." });
            }

            await _repository.UpdateTicketAsync(ticket);
            return Ok(new { message = "Ticket updated successfully." });
        }

        // DELETE: /api/Ticket/{id}
        [HttpDelete("{id:int}")]
        public async Task<IActionResult> DeleteTicket(int id)
        {
            var existingTicket = await _repository.GetTicketByIdAsync(id);
            if (existingTicket == null)
            {
                return NotFound(new { message = $"Ticket with ID {id} not found." });
            }

            await _repository.DeleteTicketAsync(id);
            return Ok(new { message = "Ticket deleted successfully." });
        }

        // GET: /api/Ticket/Status/{status}
        [HttpGet("Status/{status}")]
        public async Task<IActionResult> GetTicketsByStatus(string status)
        {
            var tickets = await _repository.GetTicketsByStatusAsync(status);
            return Ok(tickets);
        }
    }
}

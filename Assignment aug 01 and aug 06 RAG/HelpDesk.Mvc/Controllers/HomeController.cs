using Microsoft.AspNetCore.Mvc;

namespace HelpDesk.Mvc.Controllers
{
    public class HomeController : Controller
    {
        public IActionResult Index()
        {
            return RedirectToAction("Dashboard", "Ticket");
        }
    }
}

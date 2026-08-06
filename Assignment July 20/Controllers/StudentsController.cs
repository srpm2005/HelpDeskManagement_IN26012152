using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using StudentRegistration.Data;
using StudentRegistration.Models;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace StudentRegistration.Controllers
{
    [Authorize(Roles = "Admin")]
    public class StudentsController : Controller
    {
        private readonly UserManager<ApplicationUser> _userManager;
        private readonly ApplicationDbContext _context;

        public StudentsController(UserManager<ApplicationUser> userManager, ApplicationDbContext context)
        {
            _userManager = userManager;
            _context = context;
        }

        // GET: Students
        public async Task<IActionResult> Index()
        {
            // Get all users in the Student role
            var students = await _userManager.GetUsersInRoleAsync("Student");
            
            // To ensure we get the course details, let's load them from the database context
            var studentIds = students.Select(s => s.Id).ToList();
            
            var studentsWithCourses = await _context.Users
                .Include(u => u.RegisteredCourse)
                .Where(u => studentIds.Contains(u.Id))
                .ToListAsync();

            return View(studentsWithCourses);
        }
    }
}

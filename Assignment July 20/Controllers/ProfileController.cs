using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using StudentRegistration.Data;
using StudentRegistration.Models;
using System.Threading.Tasks;

namespace StudentRegistration.Controllers
{
    [Authorize(Roles = "Student")]
    public class ProfileController : Controller
    {
        private readonly UserManager<ApplicationUser> _userManager;
        private readonly ApplicationDbContext _context;

        public ProfileController(UserManager<ApplicationUser> userManager, ApplicationDbContext context)
        {
            _userManager = userManager;
            _context = context;
        }

        // GET: Profile
        public async Task<IActionResult> Index()
        {
            var user = await _userManager.GetUserAsync(User);
            if (user == null)
            {
                return Challenge();
            }

            // Load the registered course details
            var userWithCourse = await _context.Users
                .Include(u => u.RegisteredCourse)
                .FirstOrDefaultAsync(u => u.Id == user.Id);

            return View(userWithCourse);
        }

        // GET: Profile/Edit
        public async Task<IActionResult> Edit()
        {
            var user = await _userManager.GetUserAsync(User);
            if (user == null)
            {
                return Challenge();
            }

            var model = new EditProfileViewModel
            {
                FirstName = user.FirstName,
                LastName = user.LastName
            };

            return View(model);
        }

        // POST: Profile/Edit
        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> Edit(EditProfileViewModel model)
        {
            if (ModelState.IsValid)
            {
                var user = await _userManager.GetUserAsync(User);
                if (user == null)
                {
                    return Challenge();
                }

                user.FirstName = model.FirstName;
                user.LastName = model.LastName;

                var result = await _userManager.UpdateAsync(user);
                if (result.Succeeded)
                {
                    TempData["SuccessMessage"] = "Profile details updated successfully!";
                    return RedirectToAction(nameof(Index));
                }

                foreach (var error in result.Errors)
                {
                    ModelState.AddModelError(string.Empty, error.Description);
                }
            }

            return View(model);
        }

        // POST: Profile/RegisterCourse
        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> RegisterCourse(int courseId)
        {
            var user = await _userManager.GetUserAsync(User);
            if (user == null)
            {
                return Challenge();
            }

            // Reload user with current DB state to ensure concurrency check
            var dbUser = await _context.Users.FindAsync(user.Id);
            if (dbUser == null)
            {
                return NotFound();
            }

            // Rule: Register for only one course
            if (dbUser.RegisteredCourseId.HasValue)
            {
                TempData["ErrorMessage"] = "You are already registered for a course. You can only register for one course.";
                return RedirectToAction("Index", "Courses");
            }

            var course = await _context.Courses.FindAsync(courseId);
            if (course == null)
            {
                TempData["ErrorMessage"] = "The selected course does not exist.";
                return RedirectToAction("Index", "Courses");
            }

            dbUser.RegisteredCourseId = courseId;
            await _context.SaveChangesAsync();

            TempData["SuccessMessage"] = $"Successfully registered for the course: '{course.Name}'!";
            return RedirectToAction(nameof(Index));
        }
    }
}

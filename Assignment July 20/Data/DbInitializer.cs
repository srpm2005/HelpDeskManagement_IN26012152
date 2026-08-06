using Microsoft.AspNetCore.Identity;
using Microsoft.Extensions.DependencyInjection;
using StudentRegistration.Models;
using System;
using System.Linq;
using System.Threading.Tasks;

namespace StudentRegistration.Data
{
    public static class DbInitializer
    {
        public static async Task Initialize(IServiceProvider serviceProvider)
        {
            using var context = serviceProvider.GetRequiredService<ApplicationDbContext>();
            
            // Create database if not exists
            context.Database.EnsureCreated();

            var roleManager = serviceProvider.GetRequiredService<RoleManager<IdentityRole>>();
            var userManager = serviceProvider.GetRequiredService<UserManager<ApplicationUser>>();

            // 1. Seed Roles
            string[] roleNames = { "Admin", "Student" };
            foreach (var roleName in roleNames)
            {
                var roleExist = await roleManager.RoleExistsAsync(roleName);
                if (!roleExist)
                {
                    await roleManager.CreateAsync(new IdentityRole(roleName));
                }
            }

            // 2. Seed Admin User
            string adminEmail = "admin@studentreg.com";
            var adminUser = await userManager.FindByEmailAsync(adminEmail);
            if (adminUser == null)
            {
                var admin = new ApplicationUser
                {
                    UserName = adminEmail,
                    Email = adminEmail,
                    FirstName = "System",
                    LastName = "Administrator",
                    EmailConfirmed = true
                };

                var createAdminResult = await userManager.CreateAsync(admin, "AdminPassword123!");
                if (createAdminResult.Succeeded)
                {
                    await userManager.AddToRoleAsync(admin, "Admin");
                }
            }

            // 3. Seed Courses if none exist
            if (!context.Courses.Any())
            {
                var courses = new Course[]
                {
                    new Course
                    {
                        Name = "Introduction to Computer Science",
                        Credits = 4,
                        Description = "Introduction to the basic concepts of programming, algorithms, and computational thinking using Python."
                    },
                    new Course
                    {
                        Name = "Web Development with ASP.NET Core",
                        Credits = 3,
                        Description = "Building modern web applications using HTML, CSS, JavaScript, and ASP.NET Core MVC."
                    },
                    new Course
                    {
                        Name = "Database Management Systems",
                        Credits = 3,
                        Description = "Relational database concepts, SQL queries, database design, and normalization using SQL Server."
                    },
                    new Course
                    {
                        Name = "Data Structures and Algorithms",
                        Credits = 4,
                        Description = "Analysis and implementation of basic data structures including lists, stacks, queues, trees, graphs, and sorting/searching algorithms."
                    },
                    new Course
                    {
                        Name = "Introduction to Software Engineering",
                        Credits = 3,
                        Description = "Software development lifecycle, design patterns, testing, agile methodologies, and Git version control."
                    }
                };

                foreach (var course in courses)
                {
                    context.Courses.Add(course);
                }
                context.SaveChanges();
            }
        }
    }
}

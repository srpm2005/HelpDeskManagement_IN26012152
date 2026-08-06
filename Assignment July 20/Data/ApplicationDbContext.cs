using Microsoft.AspNetCore.Identity.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore;
using StudentRegistration.Models;

namespace StudentRegistration.Data
{
    public class ApplicationDbContext : IdentityDbContext<ApplicationUser>
    {
        public ApplicationDbContext(DbContextOptions<ApplicationDbContext> options)
            : base(options)
        {
        }

        public DbSet<Course> Courses { get; set; }

        protected override void OnModelCreating(ModelBuilder builder)
        {
            base.OnModelCreating(builder);

            // Configure relationship between Student (ApplicationUser) and Course
            builder.Entity<ApplicationUser>()
                .HasOne(u => u.RegisteredCourse)
                .WithMany(c => c.Students)
                .HasForeignKey(u => u.RegisteredCourseId)
                .OnDelete(DeleteBehavior.SetNull); // If course is deleted, keep student but set registration to null
        }
    }
}

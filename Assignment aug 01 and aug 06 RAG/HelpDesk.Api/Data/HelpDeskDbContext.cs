using HelpDesk.Api.Models;
using Microsoft.EntityFrameworkCore;

namespace HelpDesk.Api.Data
{
    public class HelpDeskDbContext : DbContext
    {
        public HelpDeskDbContext(DbContextOptions<HelpDeskDbContext> options) : base(options)
        {
        }

        public DbSet<Ticket> Tickets { get; set; }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            base.OnModelCreating(modelBuilder);

            // Pre-populate initial support tickets for testing and demonstration
            modelBuilder.Entity<Ticket>().HasData(
                new Ticket
                {
                    Id = 1,
                    Title = "VPN Access Issue",
                    Description = "Unable to connect to company VPN from home network after recent update.",
                    Priority = "High",
                    Status = "Open",
                    RaisedBy = "Rahul Sharma",
                    CreatedDate = new DateTime(2026, 8, 1, 10, 0, 0)
                },
                new Ticket
                {
                    Id = 2,
                    Title = "Software License Request",
                    Description = "Requesting Visual Studio Enterprise license key for the upcoming project.",
                    Priority = "Medium",
                    Status = "In Progress",
                    RaisedBy = "Priya Patel",
                    CreatedDate = new DateTime(2026, 8, 2, 11, 30, 0)
                },
                new Ticket
                {
                    Id = 3,
                    Title = "Monitor Display Flicker",
                    Description = "Secondary monitor flickers randomly when connected through the USB-C docking station.",
                    Priority = "Low",
                    Status = "Closed",
                    RaisedBy = "Amit Kumar",
                    CreatedDate = new DateTime(2026, 7, 28, 14, 15, 0)
                }
            );
        }
    }
}

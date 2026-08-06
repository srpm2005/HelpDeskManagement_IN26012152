using System.ComponentModel.DataAnnotations;

namespace HelpDesk.Mvc.Models
{
    public class Ticket
    {
        public int Id { get; set; }

        [Required(ErrorMessage = "Title is required")]
        [StringLength(100, ErrorMessage = "Title cannot exceed 100 characters")]
        public string Title { get; set; } = string.Empty;

        [Required(ErrorMessage = "Description is required")]
        public string Description { get; set; } = string.Empty;

        [Required(ErrorMessage = "Priority is required")]
        public string Priority { get; set; } = "Low"; // Low, Medium, High

        [Required(ErrorMessage = "Status is required")]
        public string Status { get; set; } = "Open";   // Open, In Progress, Closed

        [Required(ErrorMessage = "Raised By is required")]
        [Display(Name = "Raised By")]
        public string RaisedBy { get; set; } = string.Empty;

        [Display(Name = "Created Date")]
        public DateTime CreatedDate { get; set; } = DateTime.Now;
    }
}

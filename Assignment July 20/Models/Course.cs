using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;

namespace StudentRegistration.Models
{
    public class Course
    {
        public int Id { get; set; }

        [Required]
        [Display(Name = "Course Name")]
        public string Name { get; set; } = string.Empty;

        [Required]
        public string Description { get; set; } = string.Empty;

        [Required]
        [Range(1, 10, ErrorMessage = "Credits must be between 1 and 10.")]
        public int Credits { get; set; }

        // Navigation property for students registered in this course
        public virtual ICollection<ApplicationUser> Students { get; set; } = new List<ApplicationUser>();
    }
}

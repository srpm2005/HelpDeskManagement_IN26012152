namespace HelpDesk.Api.Models
{
    public class Ticket
    {
        public int Id { get; set; }
        public string Title { get; set; } = string.Empty;
        public string Description { get; set; } = string.Empty;
        public string Priority { get; set; } = "Low"; // Low, Medium, High
        public string Status { get; set; } = "Open";   // Open, In Progress, Closed
        public string RaisedBy { get; set; } = string.Empty;
        public DateTime CreatedDate { get; set; } = DateTime.Now;
    }
}

# Help Desk Ticket Management System (`HelpDeskManagement`)
## Project Submission Report & Complete Code Documentation

---

### 1. Executive Summary & Project Objective

The **Help Desk Ticket Management System (`HelpDeskManagement`)** is an enterprise-ready web application designed for managing internal employee IT support requests. Built using **ASP.NET Core 10.0 Web API**, **Entity Framework Core**, **SQL Server**, **ASP.NET Core MVC**, and **xUnit with Moq**, the system enables employees and IT support staff to create, view, filter, edit, and resolve support tickets.

---

### 2. System Architecture & Technical Stack

- **Web API Layer (`HelpDesk.Api`)**: Exposes RESTful HTTP JSON endpoints. Implements Repository Pattern (`ITicketRepository`, `TicketRepository`) and EF Core DbContext for SQL Server.
- **MVC Layer (`HelpDesk.Mvc`)**: User interface built with Razor Views and a dedicated Service Layer (`TicketService`) consuming Web API via `HttpClient`. All styling strictly follows a minimalist monochrome aesthetic (black/white contrast, square 90° edges, single regular font weight).
- **Unit Test Layer (`HelpDesk.Tests`)**: Independent test project with 13 xUnit unit tests mocking `ITicketRepository` via Moq to verify API controller logic in 100% isolation.

---

### 3. Application Screenshots & Visual Proof

![Figure 1: HelpDesk Web API Execution Logs](Screenshot%202026-08-03%20235507.png)
*Figure 1: HelpDesk Web API Execution Logs & Port Binding Verification*

![Figure 2: Help Desk System Dashboard](Screenshot%202026-08-04%20001249.png)
*Figure 2: Help Desk System Dashboard Overview (Total, Open, and Closed Ticket Cards)*

![Figure 3: Support Tickets List Table](Screenshot%202026-08-04%20001257.png)
*Figure 3: Support Tickets List Table View with Interactive Status Filters*

![Figure 4: Detailed View of Individual Support Ticket](Screenshot%202026-08-04%20001303.png)
*Figure 4: Detailed View of Individual Support Ticket*

![Figure 5: Raise New Support Ticket Form](Screenshot%202026-08-04%20001317.png)
*Figure 5: Raise New Support Ticket Form (Status Hardcoded to Open)*

![Figure 6: Edit Ticket Form](Screenshot%202026-08-04%20001326.png)
*Figure 6: Edit Ticket Form (Updating Priority & Status Drops)*

![Figure 7: Delete Ticket Confirmation Page](Screenshot%202026-08-04%20001339.png)
*Figure 7: Delete Ticket Confirmation Page*

---

### 4. REST API Endpoint Specifications

| HTTP Method | API Endpoint | Description |
| :--- | :--- | :--- |
| **GET** | `/api/Ticket/All` | Retrieve list of all support tickets |
| **GET** | `/api/Ticket/{id}` | Retrieve specific ticket details by ID |
| **POST** | `/api/Ticket` | Create a new support ticket |
| **PUT** | `/api/Ticket/{id}` | Update an existing support ticket |
| **DELETE** | `/api/Ticket/{id}` | Delete support ticket by ID |
| **GET** | `/api/Ticket/Status/{status}` | Filter support tickets by status (Open/In Progress/Closed) |

---

### 5. Unit Test Execution Results

All 13 unit test cases (6 mandatory + 7 extended/optional) were executed using **xUnit** and **Moq** against the Web API `TicketController`. 
- **Passed**: 13 / 13
- **Failed**: 0
- **Skipped**: 0

---

### 6. Complete Source Code Listings

#### `HelpDesk.Api/Models/Ticket.cs`
```csharp
namespace HelpDesk.Api.Models
{
    public class Ticket
    {
        public int Id { get; set; }
        public string Title { get; set; } = string.Empty;
        public string Description { get; set; } = string.Empty;
        public string Priority { get; set; } = "Low";
        public string Status { get; set; } = "Open";
        public string RaisedBy { get; set; } = string.Empty;
        public DateTime CreatedDate { get; set; } = DateTime.Now;
    }
}
```

#### `HelpDesk.Api/Repositories/ITicketRepository.cs`
```csharp
using HelpDesk.Api.Models;

namespace HelpDesk.Api.Repositories
{
    public interface ITicketRepository
    {
        Task<List<Ticket>> GetAllTicketsAsync();
        Task<Ticket?> GetTicketByIdAsync(int id);
        Task<int> CreateTicketAsync(Ticket ticket);
        Task UpdateTicketAsync(Ticket ticket);
        Task DeleteTicketAsync(int id);
        Task<List<Ticket>> GetTicketsByStatusAsync(string status);
    }
}
```

#### `HelpDesk.Tests/Controllers/TicketControllerTests.cs`
```csharp
using HelpDesk.Api.Controllers;
using HelpDesk.Api.Models;
using HelpDesk.Api.Repositories;
using Microsoft.AspNetCore.Mvc;
using Moq;
using Xunit;

namespace HelpDesk.Tests.Controllers
{
    public class TicketControllerTests
    {
        private readonly Mock<ITicketRepository> _mockRepo;
        private readonly TicketController _controller;

        public TicketControllerTests()
        {
            _mockRepo = new Mock<ITicketRepository>();
            _controller = new TicketController(_mockRepo.Object);
        }

        [Fact]
        public async Task GetAllTickets_ReturnsOkResult_WhenTicketExist()
        {
            var sampleTickets = new List<Ticket>
            {
                new Ticket { Id = 1, Title = "VPN Issue", Priority = "High", Status = "Open", RaisedBy = "Rahul" }
            };
            _mockRepo.Setup(repo => repo.GetAllTicketsAsync()).ReturnsAsync(sampleTickets);
            var result = await _controller.GetAllTickets();
            Assert.IsType<OkObjectResult>(result);
        }
    }
}
```

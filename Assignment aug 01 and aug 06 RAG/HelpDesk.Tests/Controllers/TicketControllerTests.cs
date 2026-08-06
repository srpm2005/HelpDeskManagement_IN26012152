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

        // ==========================================
        // Mandatory Test Cases (1 to 6)
        // ==========================================

        [Fact]
        public async Task GetAllTickets_ReturnsOkResult_WhenTicketExist()
        {
            // Arrange
            var sampleTickets = new List<Ticket>
            {
                new Ticket { Id = 1, Title = "VPN Issue", Priority = "High", Status = "Open", RaisedBy = "Rahul" },
                new Ticket { Id = 2, Title = "License Request", Priority = "Low", Status = "Closed", RaisedBy = "Priya" }
            };
            _mockRepo.Setup(repo => repo.GetAllTicketsAsync()).ReturnsAsync(sampleTickets);

            // Act
            var result = await _controller.GetAllTickets();

            // Assert
            var okResult = Assert.IsType<OkObjectResult>(result);
            var returnedTickets = Assert.IsAssignableFrom<List<Ticket>>(okResult.Value);
            Assert.Equal(2, returnedTickets.Count);
        }

        [Fact]
        public async Task GetTicketById_ReturnsOkResult_WhenTicketExists()
        {
            // Arrange
            var ticket = new Ticket { Id = 1, Title = "VPN Issue", Priority = "High", Status = "Open", RaisedBy = "Rahul" };
            _mockRepo.Setup(repo => repo.GetTicketByIdAsync(1)).ReturnsAsync(ticket);

            // Act
            var result = await _controller.GetTicketById(1);

            // Assert
            var okResult = Assert.IsType<OkObjectResult>(result);
            var returnedTicket = Assert.IsType<Ticket>(okResult.Value);
            Assert.Equal(1, returnedTicket.Id);
            Assert.Equal("VPN Issue", returnedTicket.Title);
        }

        [Fact]
        public async Task GetTicketById_ReturnsNotFound_WhenTicketDoesNotExist()
        {
            // Arrange
            _mockRepo.Setup(repo => repo.GetTicketByIdAsync(999)).ReturnsAsync((Ticket?)null);

            // Act
            var result = await _controller.GetTicketById(999);

            // Assert
            Assert.IsType<NotFoundObjectResult>(result);
        }

        [Fact]
        public async Task CreateTicket_ReturnsOkResult_WhenTicketIsCreatedSuccessfully()
        {
            // Arrange
            var newTicket = new Ticket { Title = "Printer Offline", Description = "3rd floor printer", Priority = "Medium", Status = "Open", RaisedBy = "Amit" };
            _mockRepo.Setup(repo => repo.CreateTicketAsync(newTicket)).ReturnsAsync(10);

            // Act
            var result = await _controller.CreateTicket(newTicket);

            // Assert
            var okResult = Assert.IsType<OkObjectResult>(result);
            Assert.Equal(10, okResult.Value);
        }

        [Fact]
        public async Task CreateTicket_ReturnsBadRequest_WhenTicketIsNull()
        {
            // Act
            var result = await _controller.CreateTicket(null);

            // Assert
            Assert.IsType<BadRequestObjectResult>(result);
        }

        [Fact]
        public async Task GetTicketsByStatus_ReturnsOkResult_WhenMatchingTicketsExist()
        {
            // Arrange
            var openTickets = new List<Ticket>
            {
                new Ticket { Id = 1, Title = "VPN Issue", Status = "Open" },
                new Ticket { Id = 3, Title = "Network Slow", Status = "Open" }
            };
            _mockRepo.Setup(repo => repo.GetTicketsByStatusAsync("Open")).ReturnsAsync(openTickets);

            // Act
            var result = await _controller.GetTicketsByStatus("Open");

            // Assert
            var okResult = Assert.IsType<OkObjectResult>(result);
            var returnedTickets = Assert.IsAssignableFrom<List<Ticket>>(okResult.Value);
            Assert.Equal(2, returnedTickets.Count);
        }

        // ==========================================
        // Optional Test Cases (7 to 12)
        // ==========================================

        [Fact]
        public async Task UpdateTicket_ReturnsOkResult_WhenUpdateIsSuccessful()
        {
            // Arrange
            var existingTicket = new Ticket { Id = 1, Title = "VPN Issue", Status = "Open" };
            var updatedTicket = new Ticket { Id = 1, Title = "VPN Issue Fixed", Status = "Closed" };

            _mockRepo.Setup(repo => repo.GetTicketByIdAsync(1)).ReturnsAsync(existingTicket);
            _mockRepo.Setup(repo => repo.UpdateTicketAsync(updatedTicket)).Returns(Task.CompletedTask);

            // Act
            var result = await _controller.UpdateTicket(1, updatedTicket);

            // Assert
            Assert.IsType<OkObjectResult>(result);
        }

        [Fact]
        public async Task UpdateTicket_ReturnsNotFound_WhenTicketDoesNotExist()
        {
            // Arrange
            var updatedTicket = new Ticket { Id = 999, Title = "Non-existent Ticket", Status = "Closed" };
            _mockRepo.Setup(repo => repo.GetTicketByIdAsync(999)).ReturnsAsync((Ticket?)null);

            // Act
            var result = await _controller.UpdateTicket(999, updatedTicket);

            // Assert
            Assert.IsType<NotFoundObjectResult>(result);
        }

        [Fact]
        public async Task DeleteTicket_ReturnsOkResult_WhenTicketIsDeletedSuccessfully()
        {
            // Arrange
            var existingTicket = new Ticket { Id = 1, Title = "VPN Issue", Status = "Open" };
            _mockRepo.Setup(repo => repo.GetTicketByIdAsync(1)).ReturnsAsync(existingTicket);
            _mockRepo.Setup(repo => repo.DeleteTicketAsync(1)).Returns(Task.CompletedTask);

            // Act
            var result = await _controller.DeleteTicket(1);

            // Assert
            Assert.IsType<OkObjectResult>(result);
        }

        [Fact]
        public async Task DeleteTicket_ReturnsNotFound_WhenTicketDoesNotExist()
        {
            // Arrange
            _mockRepo.Setup(repo => repo.GetTicketByIdAsync(999)).ReturnsAsync((Ticket?)null);

            // Act
            var result = await _controller.DeleteTicket(999);

            // Assert
            Assert.IsType<NotFoundObjectResult>(result);
        }

        [Fact]
        public async Task GetAllTickets_ReturnEmptyList_WhenNoTicketExist()
        {
            // Arrange
            _mockRepo.Setup(repo => repo.GetAllTicketsAsync()).ReturnsAsync(new List<Ticket>());

            // Act
            var result = await _controller.GetAllTickets();

            // Assert
            var okResult = Assert.IsType<OkObjectResult>(result);
            var returnedTickets = Assert.IsAssignableFrom<List<Ticket>>(okResult.Value);
            Assert.Empty(returnedTickets);
        }

        [Fact]
        public async Task GetTicketsByStatus_ReturnEmptyList_WhenNoMatchingTicketsExist()
        {
            // Arrange
            _mockRepo.Setup(repo => repo.GetTicketsByStatusAsync("Closed")).ReturnsAsync(new List<Ticket>());

            // Act
            var result = await _controller.GetTicketsByStatus("Closed");

            // Assert
            var okResult = Assert.IsType<OkObjectResult>(result);
            var returnedTickets = Assert.IsAssignableFrom<List<Ticket>>(okResult.Value);
            Assert.Empty(returnedTickets);
        }
    }
}

using System.Net.Http.Json;
using HelpDesk.Mvc.Models;

namespace HelpDesk.Mvc.Services
{
    public class TicketService
    {
        private readonly HttpClient _httpClient;

        public TicketService(HttpClient httpClient)
        {
            _httpClient = httpClient;
        }

        public async Task<List<Ticket>> GetAllTicketsAsync()
        {
            try
            {
                var tickets = await _httpClient.GetFromJsonAsync<List<Ticket>>("api/Ticket/All");
                return tickets ?? new List<Ticket>();
            }
            catch
            {
                return new List<Ticket>();
            }
        }

        public async Task<Ticket?> GetTicketByIdAsync(int id)
        {
            try
            {
                return await _httpClient.GetFromJsonAsync<Ticket>($"api/Ticket/{id}");
            }
            catch
            {
                return null;
            }
        }

        public async Task<bool> CreateTicketAsync(Ticket ticket)
        {
            try
            {
                var response = await _httpClient.PostAsJsonAsync("api/Ticket", ticket);
                return response.IsSuccessStatusCode;
            }
            catch
            {
                return false;
            }
        }

        public async Task<bool> UpdateTicketAsync(Ticket ticket)
        {
            try
            {
                var response = await _httpClient.PutAsJsonAsync($"api/Ticket/{ticket.Id}", ticket);
                return response.IsSuccessStatusCode;
            }
            catch
            {
                return false;
            }
        }

        public async Task<bool> DeleteTicketAsync(int id)
        {
            try
            {
                var response = await _httpClient.DeleteAsync($"api/Ticket/{id}");
                return response.IsSuccessStatusCode;
            }
            catch
            {
                return false;
            }
        }

        public async Task<List<Ticket>> GetTicketsByStatusAsync(string status)
        {
            try
            {
                var tickets = await _httpClient.GetFromJsonAsync<List<Ticket>>($"api/Ticket/Status/{Uri.EscapeDataString(status)}");
                return tickets ?? new List<Ticket>();
            }
            catch
            {
                return new List<Ticket>();
            }
        }
    }
}

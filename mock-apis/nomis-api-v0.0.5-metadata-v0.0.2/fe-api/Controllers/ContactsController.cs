using System;
using System.Collections.Generic;
using System.Threading.Tasks;

using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Logging;
using Microsoft.AspNetCore.Http;

using Nomis.Interfaces.Contacts.Models;
using Nomis.Interfaces.Contacts.Repository;
using Nomis.Interfaces.Core.Models;

namespace fe_api.Controllers
{
    [ApiController]
    [Route("[controller]")]
    public class ContactsController : ControllerBase
    {
        private readonly ILogger<ContactsController> _logger;
        private readonly IContactStore _contacts;

        public ContactsController(ILogger<ContactsController> logger, IContactStore contacts)
        {
            _logger = logger;
            _contacts = contacts;
        }

        /// <summary>Get a list of all contacts.</summary>
        /// <remarks>Get a list of all contacts that can be assigned to datasets.</remarks>
        /// <param name="q">Query using Lucene syntax (e.g. `name:census OR email:support@example.com`).</param>
        /// <returns>List of contacts.</returns>
        [HttpGet]
        [ProducesResponseType(StatusCodes.Status200OK)]
        public async Task<ActionResult<IEnumerable<Contact>>> GetAllContacts([FromQuery(Name = "q")] string q)
        {
            QueryFilterOptions options = new QueryFilterOptions() {
                Query = { Value = q, Syntax = Syntax.Lucene }
            };

            return Ok(await _contacts.GetAllAsync(options));
        }

        /// <summary>Get details of a contact.</summary>
        /// <remarks>Get details of a contact that can be assigned to datasets.</remarks>
        /// <param name="id">Id of the contact.</param>
        /// <returns>Contact details.</returns>
        [HttpGet("{id}")]
        [ProducesResponseType(StatusCodes.Status200OK)]
        [ProducesResponseType(StatusCodes.Status404NotFound)]
        public async Task<ActionResult<Contact>> GetContactById(string id) {
            var contact = await _contacts.GetAsync(id);
            if(contact == null) return NotFound("Contact not found.");
            else return Ok(contact);
        }

        /// <summary>Create or update a contact.</summary>
        /// <remarks>Create or update a contact that can be assigned to datasets.</remarks>
        /// <param name="id">Id of the contact.</param>
        /// <param name="contact">Object representing the contact.</param>
        /// <returns>Contact details.</returns>
        [HttpPut("{id}")]
        [ProducesResponseType(StatusCodes.Status201Created)]
        [ProducesResponseType(StatusCodes.Status400BadRequest)]
        [ProducesResponseType(StatusCodes.Status403Forbidden)]
        [ProducesResponseType(StatusCodes.Status500InternalServerError)]
        public async Task<ActionResult<Contact>> PutContactById(string id, Contact contact) {
            if(id != contact.Id) return BadRequest("Resource and contact Id mismatched");
            
            try {
                var added = await _contacts.AddAsync(contact);
                return CreatedAtAction(nameof(GetContactById), new { id = contact.Id }, contact);
            }
            catch(Exception ex) {
                if(ex is UnauthorizedAccessException) return Forbid(ex.Message);
                else return StatusCode(StatusCodes.Status500InternalServerError, ex.Message);
            }
        }

        /// <summary>Partial update of a contact.</summary>
        /// <remarks>Partial update of a contact that can be assigned to datasets.</remarks>
        /// <param name="id">Id of the contact.</param>
        /// <param name="contact">Partial object representing the contact.</param>
        /// <returns>Contact details.</returns>
        [HttpPatch("{id}")]
        [ProducesResponseType(StatusCodes.Status200OK)]
        [ProducesResponseType(StatusCodes.Status400BadRequest)]
        [ProducesResponseType(StatusCodes.Status403Forbidden)]
        [ProducesResponseType(StatusCodes.Status500InternalServerError)]
        public async Task<ActionResult<Contact>> PatchContactById(string id, Contact contact) {
            if(id != contact.Id) return BadRequest("Resource and contact Id mismatched");

            try {
                var updated = await _contacts.UpdateAsync(contact);
                return Ok(updated);
            }
            catch(Exception ex) {
                if(ex is UnauthorizedAccessException) return Forbid(ex.Message);
                else return StatusCode(StatusCodes.Status500InternalServerError, ex.Message);
            }
        }

        /// <summary>Delete a contact.</summary>
        /// <remarks>Delete a contact, if the contact is assigned to a dataset, the operation will fail.</remarks>
        /// <param name="id">Id of the contact.</param>
        [HttpDelete("{id}")]
        [ProducesResponseType(StatusCodes.Status204NoContent)]
        [ProducesResponseType(StatusCodes.Status403Forbidden)]
        [ProducesResponseType(StatusCodes.Status404NotFound)]
        [ProducesResponseType(StatusCodes.Status409Conflict)]
        [ProducesResponseType(StatusCodes.Status500InternalServerError)]
        public async Task<ActionResult<Contact>> DeleteContactById(string id) {
            try
            {
                // See if the contact exists.
                var contact = await _contacts.GetAsync(id);
                if(contact == null) return NotFound();

                // Attempt to delete the contact.
                if(await _contacts.DeleteAsync(id)) return NoContent();
                else return Conflict();
            }
            catch(Exception ex) {
                if(ex is UnauthorizedAccessException) return Forbid(ex.Message);
                else return StatusCode(StatusCodes.Status500InternalServerError, ex.Message);
            }
        }
    }
}

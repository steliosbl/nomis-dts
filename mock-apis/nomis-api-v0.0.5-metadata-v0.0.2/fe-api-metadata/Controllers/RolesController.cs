using System.Collections.Generic;
using System.Threading.Tasks;

using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Logging;
using Microsoft.AspNetCore.Http;

using Nomis.Interfaces.Metadata.Models;
using Nomis.Interfaces.Metadata.Repository;

namespace Nomis.Api.Metadata.Controllers
{
    [ApiController]
    [Route("[controller]")]
    public class RolesController : ControllerBase
    {
        private readonly ILogger<RolesController> _logger;
        private readonly IMetaRoleStore _context;

        public RolesController(
            ILogger<RolesController> logger,
            IMetaRoleStore context)
        {
            _logger = logger;
            _context = context;
        }

        /// <summary>Get all roles.</summary>
        /// <remarks>Get a complete list of all defined metadata roles. These entries can be used in metadata property groups.</remarks>
        /// <returns>List of roles.</returns>
        [ProducesResponseType(StatusCodes.Status200OK)]
        [HttpGet]
        public async Task<ActionResult<IEnumerable<MetaItemRole>>> GetAllAsync() {
            var ns = await _context.GetAllAsync();

            if(ns == null) return Ok(new List<MetaItemRole>());
            else return Ok(ns);
        }

        /// <summary>Get a specific metadata role.</summary>
        /// <remarks>Get a specific metadata role for use with metadata property groups.</remarks>
        /// <param name="role">Unique ID of the role.</param>
        /// <returns>Metadata role.</returns>
        [ProducesResponseType(StatusCodes.Status200OK)]
        [ProducesResponseType(StatusCodes.Status404NotFound)]
        [HttpGet("{role}", Name = "GetRoleByIdAsync")]
        public async Task<ActionResult<MetaItemRole>> GetRoleByIdAsync(string role) {
            var ns = await _context.GetAsync(role);

            if(ns == null) return NotFound();
            else return Ok(ns);
        }

        /// <summary>Create/update a role.</summary>
        /// <remarks>Create or update a role for use with metadata property groups.</remarks>
        /// <param name="role">Unique ID of the role.</param>
        /// <param name="metaItemRole">Object representing the role.</param>
        /// <returns>Metadata role.</returns>
        [ProducesResponseType(StatusCodes.Status201Created)]
        [ProducesResponseType(StatusCodes.Status409Conflict)]
        [HttpPut("{role}")]
        public async Task<ActionResult<MetaItemRole>> PutAsync(string role, MetaItemRole metaItemRole) {
            if(metaItemRole.Role != role) return BadRequest("Object prefix and path mismatched.");

            if(await _context.AddAsync(metaItemRole)) return CreatedAtRoute("GetRoleByIdAsync", new { Role = metaItemRole.Role }, metaItemRole);
            else return Conflict();
        }

        /// <summary>Delete a role.</summary>
        /// <remarks>Delete a metadata group role. Warning: any metadata groups using this rolse will also be deleted.</remarks>
        /// <param name="role">Unique ID of the role (e.g. `note`).</param>
        [ProducesResponseType(StatusCodes.Status204NoContent)]
        [ProducesResponseType(StatusCodes.Status409Conflict)]
        [HttpDelete("{role}")]
        public async Task<IActionResult> DeleteAsync(string role) {
            if(await _context.DeleteAsync(role)) return NoContent();
            else return Conflict();
        }
    }
}
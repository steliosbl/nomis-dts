using System;
using System.Collections.Generic;
using System.Threading.Tasks;

using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Logging;
using Microsoft.AspNetCore.Http;

using Nomis.Interfaces.Core.Helpers;
using Nomis.Interfaces.Core.Models;
using Nomis.Interfaces.Metadata.Models;
using Nomis.Interfaces.Metadata.Repository;

namespace Nomis.Api.Metadata.Controllers
{
    [ApiController]
    [Route("[controller]")]
    public class DefinitionsController : ControllerBase
    {
        private readonly ILogger<DefinitionsController> _logger;
        private readonly IMetadataStore _context;

        public DefinitionsController(
            ILogger<DefinitionsController> logger,
            IMetadataStore context)
        {
            _logger = logger;
            _context = context;
        }

        /// <summary>Get unresolved metadata.</summary>
        /// <remarks>
        ///     Get a list of all metadata, as defined, without resolving the `Include` entries. The response
        ///     from this endpoint is suitable for modification and subsequent use in calls to `POST`.
        /// </remarks>
        /// <param name="q">Query to filter results (e.g. `description:census`).</param>
        /// <returns>List of unresolved metadata.</returns>
        [HttpGet(Name = "GetDefinitionsAsync")]
        [ProducesResponseType(StatusCodes.Status200OK)]
        [ProducesResponseType(StatusCodes.Status404NotFound)]
        public async Task<ActionResult<IEnumerable<MetaAssociation>>> GetDefinitionsAsync(string q) {
            QueryFilterOptions options = null;
            if(!string.IsNullOrEmpty(q)) options = new QueryFilterOptions() { Query = new FilterValue<string>() { Value = q }};

            var meta = await _context.GetAllAsync(options);

            if(meta == null) return Ok(new List<MetaAssociation>());
            else return Ok(meta);
        }

        /// <summary>Add some metadata.</summary>
        /// <remarks>Create some new metadata</remarks>
        /// <param name="list">List of metadata associations to add.</param>
        /// <returns>List of metadata definitions added.</returns>
        [HttpPost]
        [ProducesResponseType(StatusCodes.Status200OK)]
        [ProducesResponseType(StatusCodes.Status409Conflict)]
        public async Task<ActionResult<List<MetaAssociation>>> PostAsync(List<MetaAssociation> list) {
            List<MetaAssociation> results = new List<MetaAssociation>();

            foreach(var meta in list) {
                if(meta.Id == null) meta.Id = Guid.NewGuid();
                if(meta.Created == null) meta.Created = DateTime.Now;

                results.Add(await _context.AddAsync(meta));
            }

            return Ok(results);
        }

        /// <summary>Get a specific metadata association definition.</summary>
        /// <remarks>
        ///     Get a single item of metadata, as defined, without resolving the `Include` entries. The response
        ///     from this endpoint is suitable for modification and subsequent use in calls to `PUT`.
        /// </remarks>
        /// <param name="id">UUID of metadata.</param>
        /// <returns>Metadata association.</returns>
        [HttpGet("{id}", Name = "GetDefinitionByIdAsync")]
        [ProducesResponseType(StatusCodes.Status200OK)]
        [ProducesResponseType(StatusCodes.Status404NotFound)]
        public async Task<ActionResult<MetaAssociation>> GetDefinitionByIdAsync(Guid id) {
            var meta = await _context.GetAsync(id);

            if(meta == null) return NotFound();
            else return Ok(meta);
        }

        /// <summary>Create/update a metadata association.</summary>
        /// <remarks>Create or update a single metadata association definition.</remarks>
        /// <param name="id">UUID identifying the metadata item.</param>
        /// <param name="meta">Object representing the metadata.</param>
        /// <returns>Updated metadata definition.</returns>
        [HttpPut("{id}")]
        [ProducesResponseType(StatusCodes.Status201Created)]
        [ProducesResponseType(StatusCodes.Status400BadRequest)]
        [ProducesResponseType(StatusCodes.Status409Conflict)]
        public async Task<ActionResult<MetaAssociation>> PutAsync(Guid id, MetaAssociation meta) {
            if(meta.Id != id) return BadRequest("Object Id and path mismatched.");

            var result = await _context.AddAsync(meta);

            if(result != null) return CreatedAtRoute("GetDefinitionByIdAsync", new { Id = result.Id }, result);
            else return Conflict(meta);
        }

        /// <summary>Delete a specific metadata association.</summary>
        /// <remarks>Remove a single metadata association definition, and all its properties.</remarks>
        /// <param name="id">UUID of the association to delete.</param>
        [HttpDelete("{id}")]
        [ProducesResponseType(StatusCodes.Status204NoContent)]
        [ProducesResponseType(StatusCodes.Status409Conflict)]
        public async Task<IActionResult> DeleteAsync(Guid id) {
            if(await _context.DeleteAsync(id)) return NoContent();
            else return Conflict();
        }
    }
}
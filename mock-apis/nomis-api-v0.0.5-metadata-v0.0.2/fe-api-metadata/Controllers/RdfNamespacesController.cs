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
    [Route("Rdf-Namespaces")]
    public class RdfNamespacesController : ControllerBase
    {
        private readonly ILogger<RdfNamespacesController> _logger;
        private readonly IRdfNamespaceStore _context;

        public RdfNamespacesController(
            ILogger<RdfNamespacesController> logger,
            IRdfNamespaceStore context)
        {
            _logger = logger;
            _context = context;
        }

        /// <summary>Get RDF namespaces.</summary>
        /// <remarks>Get a complete list of all defined RDF namespace entries. These entries can be used in metadata properties.</remarks>
        /// <returns>List of RDF namespaces.</returns>
        [ProducesResponseType(StatusCodes.Status200OK)]
        [HttpGet]
        public async Task<ActionResult<IEnumerable<RdfNamespace>>> GetAllAsync() {
            var ns = await _context.GetAllAsync();

            if(ns == null) return Ok(new List<RdfNamespace>());
            else return Ok(ns);
        }

        /// <summary>Get a specific RDF namespace.</summary>
        /// <remarks>Get an RDF namespace entry.</remarks>
        /// <param name="prefix">Short prefix used to uniquely identify the namespace (e.g. `dc`).</param>
        /// <returns>RDF namespace matching prefix.</returns>
        [ProducesResponseType(StatusCodes.Status200OK)]
        [ProducesResponseType(StatusCodes.Status404NotFound)]
        [HttpGet("{prefix}", Name = "GetRdfNamespaceByPrefixAsync")]
        public async Task<ActionResult<RdfNamespace>> GetRdfNamespaceByPrefixAsync(string prefix) {
            var ns = await _context.GetAsync(prefix);

            if(ns == null) return NotFound();
            else return Ok(ns);
        }

        /// <summary>Create/update an RDF namespace.</summary>
        /// <remarks>Create or update an RDF namespace for use with metadata properties.</remarks>
        /// <param name="prefix">Short prefix used to uniquely identify the namespace (e.g. `dc`).</param>
        /// <param name="rdf">Definition of an RDF namespace and URL for its schema definition.</param>
        /// <returns>RDF namespace that was created.</returns>
        [ProducesResponseType(StatusCodes.Status201Created)]
        [ProducesResponseType(StatusCodes.Status409Conflict)]
        [ProducesResponseType(StatusCodes.Status400BadRequest)]
        [HttpPut("{prefix}")]
        public async Task<ActionResult<RdfNamespace>> PutAsync(string prefix, RdfNamespace rdf) {
            if(rdf.Prefix != prefix) return BadRequest("Object prefix and path mismatched.");

            if(await _context.AddAsync(rdf)) return CreatedAtRoute("GetRdfNamespaceByPrefixAsync", new { Prefix = rdf.Prefix }, rdf);
            else return Conflict();
        }

        /// <summary>Delete an RDF namespace.</summary>
        /// <remarks>Delete an RDF namespace. Warning: any metadata properties using this namespace will also be deleted.</remarks>
        /// <param name="prefix">Short prefix used to uniquely identify the namespace (e.g. `dc`).</param>
        [ProducesResponseType(StatusCodes.Status204NoContent)]
        [ProducesResponseType(StatusCodes.Status409Conflict)]
        [HttpDelete("{prefix}")]
        public async Task<IActionResult> DeleteAsync(string prefix) {
            if(await _context.DeleteAsync(prefix)) return NoContent();
            else return Conflict();
        }
    }
}
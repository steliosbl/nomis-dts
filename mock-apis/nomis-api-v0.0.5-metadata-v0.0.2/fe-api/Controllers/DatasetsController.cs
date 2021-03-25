using System;
using System.Collections.Generic;
using System.Threading.Tasks;

using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Logging;

using Nomis.Interfaces.Datasets.Models;
using Nomis.Interfaces.Datasets.Repository;
using Nomis.Interfaces.Core.Models;

namespace fe_api.Controllers
{
    [ApiController]
    [Route("[controller]")]
    public class DatasetsController : ControllerBase
    {
        private readonly ILogger<DatasetsController> _logger;
        private readonly IDatasetStore _datasets;
        private readonly IDimensionStore _dimensions;
        private readonly IObservationStore _observations;
        private readonly IUnitStore _units;
        private readonly IStatusStore _status;

        public DatasetsController(  ILogger<DatasetsController> logger,
                                    IDatasetStore datasets,
                                    IDimensionStore dimensions,
                                    IObservationStore observations,
                                    IUnitStore units,
                                    IStatusStore status)
        {
            _logger = logger;
            _datasets = datasets;
            _dimensions = dimensions;
            _observations = observations;
            _units = units;
            _status = status;
        }

        /// <summary>
        /// Get a list of all datasets.
        /// </summary>
        /// <remarks>Provides access to the complete list of datasets available based on access permissions of guest, or authenticated user.</remarks>
        /// <param name="q">Query using Lucene syntax (e.g. `name:Claimant OR name:JSA`).</param>
        /// <returns>A list of datasets.</returns>
        [HttpGet]
        [ProducesResponseType(StatusCodes.Status200OK)]
        [ProducesResponseType(StatusCodes.Status400BadRequest)]
        public async Task<ActionResult<IEnumerable<Dataset>>> GetAllDatasetsAsync([FromQuery(Name = "q")] string q)
        {
            QueryFilterOptions options = new QueryFilterOptions() {
                Query = { Value = q, Syntax = Syntax.Lucene }
            };

            return Ok(await _datasets.GetAllAsync(options));
        }

        /// <summary>
        /// Get dataset definitiion.
        /// </summary>
        /// <remarks>Obtain the definition for a specific dataset.</remarks>
        /// <param name="id">Id of the dataset.</param>
        /// <returns>Dataset details.</returns>
        [HttpGet("{id}")]
        [ProducesResponseType(StatusCodes.Status200OK)]
        [ProducesResponseType(StatusCodes.Status400BadRequest)]
        [ProducesResponseType(StatusCodes.Status403Forbidden)]
        [ProducesResponseType(StatusCodes.Status404NotFound)]
        public async Task<ActionResult<Dataset>> GetDatasetByIdAsync(string id) {
            var dataset = await _datasets.GetAsync(id);
            if(dataset == null) return NotFound();
            else return Ok(dataset);
        }

        /// <summary>
        /// Update/create a dataset.
        /// </summary>
        /// <remarks>Update/create a dataset.</remarks>
        /// <param name="id">Id of the dataset.</param>
        /// <param name="dataset">Object representing the dataset.</param>
        /// <returns>Dataset details.</returns>
        [HttpPut("{id}")]
        [ProducesResponseType(StatusCodes.Status200OK)]
        [ProducesResponseType(StatusCodes.Status400BadRequest)]
        [ProducesResponseType(StatusCodes.Status403Forbidden)]
        [ProducesResponseType(StatusCodes.Status500InternalServerError)]
        public async Task<ActionResult<Dataset>> PutDatasetByIdAsync(string id, Dataset dataset) {
            if(id != dataset.Id) return BadRequest("Resource and dataset Id mismatched");

            try {
                Dataset ds;

                // Already exists?
                if(await _datasets.GetAsync(id) != null) {
                    ds = await _datasets.UpdateAsync(dataset);
                }
                else ds = await _datasets.AddAsync(dataset);

                if(ds != null) return Ok(ds);
                else return Conflict();
            }
            catch(Exception ex) {
                if(ex is UnauthorizedAccessException) return Forbid(ex.Message);
                else return StatusCode(StatusCodes.Status500InternalServerError, ex.Message);
            }
        }

        /// <summary>
        /// Partial update of dataset attributes.
        /// </summary>
        /// <remarks>Partial update of dataset attributes.</remarks>
        /// <param name="id">Id of the dataset.</param>
        /// <param name="dataset">Object representing the dataset.</param>
        /// <returns>Dataset details.</returns>
        [HttpPatch("{id}")]
        [ProducesResponseType(StatusCodes.Status200OK)]
        [ProducesResponseType(StatusCodes.Status400BadRequest)]
        [ProducesResponseType(StatusCodes.Status403Forbidden)]
        [ProducesResponseType(StatusCodes.Status404NotFound)]
        [ProducesResponseType(StatusCodes.Status500InternalServerError)]
        public async Task<ActionResult<Dataset>> PatchDatasetByIdAsync(string id, Dataset dataset) {
            if(id != dataset.Id) return BadRequest("Resource and dataset Id mismatched");

            try {
                var updated = await _datasets.UpdateAsync(dataset);
                return Ok(updated);
            }
            catch(Exception ex) {
                if(ex is UnauthorizedAccessException) return Forbid(ex.Message);
                else return StatusCode(StatusCodes.Status500InternalServerError, ex.Message);
            }
        }

        /// <summary>Delete the dataset.</summary>
        /// <remarks>Delete the dataset.</remarks>
        /// <param name="id">Id of the dataset.</param>
        [HttpDelete("{id}")]
        [ProducesResponseType(StatusCodes.Status204NoContent)]
        [ProducesResponseType(StatusCodes.Status403Forbidden)]
        [ProducesResponseType(StatusCodes.Status404NotFound)]
        [ProducesResponseType(StatusCodes.Status409Conflict)]
        [ProducesResponseType(StatusCodes.Status500InternalServerError)]
        public async Task<ActionResult<Dataset>> DeleteDatasetByIdAsync(string id) {
            try
            {
                // See if the contact exists.
                var dataset = await _datasets.GetAsync(id);
                if(dataset == null) return NotFound();

                // Attempt to delete the contact.
                if(await _datasets.DeleteAsync(id)) return NoContent();
                else return Conflict();
            }
            catch(Exception ex) {
                if(ex is UnauthorizedAccessException) return Forbid(ex.Message);
                else return StatusCode(StatusCodes.Status500InternalServerError, ex.Message);
            }
        }

        /// <summary>
        /// List dimensions available from a dataset.
        /// </summary>
        /// <remarks>Obtain a list of all dimensions of this dataset.</remarks>
        /// <param name="id">Id of the dataset.</param>
        /// <param name="q">Query using Lucene syntax (e.g. `name:age OR label:Marital`).</param>
        /// <returns>A list of dimensions.</returns>
        [HttpGet("{id}/dimensions")]
        [ProducesResponseType(StatusCodes.Status200OK)]
        [ProducesResponseType(StatusCodes.Status400BadRequest)]
        [ProducesResponseType(StatusCodes.Status403Forbidden)]
        [ProducesResponseType(StatusCodes.Status404NotFound)]
        public async Task<ActionResult<IEnumerable<Dimension>>> GetDimensionsForDatasetAsync(string id, [FromQuery(Name = "q")] string q) {
            QueryFilterOptions options = new QueryFilterOptions() {
                Query = { Value = q, Syntax = Syntax.Lucene }
            };

            var dimensions = await _dimensions.GetAllAsync(id, options);
            if(dimensions == null) return NotFound();
            else return Ok(dimensions);
        }

        /// <summary>
        /// Assign dimensions to this dataset.
        /// </summary>
        /// <remarks>Create or update dimensions (this set replaces any existing dimension assignments).</remarks>
        /// <param name="id">Id of the dataset.</param>
        /// <param name="dimensions">Array of objects representing the dimensions.</param>
        /// <returns>Objects representing dimensions.</returns>
        [HttpPut("{id}/dimensions")]
        [ProducesResponseType(StatusCodes.Status200OK)]
        [ProducesResponseType(StatusCodes.Status400BadRequest)]
        [ProducesResponseType(StatusCodes.Status403Forbidden)]
        [ProducesResponseType(StatusCodes.Status409Conflict)]
        [ProducesResponseType(StatusCodes.Status500InternalServerError)]
        public async Task<ActionResult<IEnumerable<Dimension>>> PutDimensionsByIdAsync(string id, Dimension[] dimensions) {
            if(dimensions == null || dimensions.Length == 0) return BadRequest("List of Dimension objects must be specified.");

            try {
                // Get current list of all dimensions in dataset.
                IEnumerable<Dimension> old = await _dimensions.GetAllAsync(id, null);
                List<Dimension> toDelete = new List<Dimension>();

                // Work out which dimensions to remove.
                if(old != null) {
                    foreach(var dimension in old) toDelete.Add(dimension);
                }

                // Remove the existing dimensions.
                foreach(var dimension in toDelete) if(!await _dimensions.DeleteAsync(id, dimension.Name)) return Conflict();

                // Add the new dimensions to the dataset.
                foreach(var dimension in dimensions) await _dimensions.AddAsync(id, dimension);

                // Return the new dimensions as they now stand.
                return Ok(await _dimensions.GetAllAsync(id, null));
            }
            catch(Exception ex) {
                if(ex is UnauthorizedAccessException) return Forbid(ex.Message);
                else return StatusCode(StatusCodes.Status500InternalServerError, ex.Message);
            }
        }

        /// <summary>
        /// Delete all dataset dimensions.
        /// </summary>
        /// <remarks>Delete all dimension assignments for this dataset (deletes dimension only, does not delete associated variable).</remarks>
        /// <param name="id">Id of the dataset.</param>
        [HttpDelete("{id}/dimensions")]
        [ProducesResponseType(StatusCodes.Status204NoContent)]
        [ProducesResponseType(StatusCodes.Status400BadRequest)]
        [ProducesResponseType(StatusCodes.Status403Forbidden)]
        [ProducesResponseType(StatusCodes.Status409Conflict)]
        [ProducesResponseType(StatusCodes.Status500InternalServerError)]
        public async Task<ActionResult> DeleteDimensionsByIdAsync(string id) {
            try {
                // Get current list of all dimensions in dataset.
                IEnumerable<Dimension> old = await _dimensions.GetAllAsync(id, null);

                // Remove the existing dimensions.
                foreach(var dimension in old) if(!await _dimensions.DeleteAsync(id, dimension.Name)) return Conflict();

                // Return success.
                return NoContent();
            }
            catch(Exception ex) {
                if(ex is UnauthorizedAccessException) return Forbid(ex.Message);
                else return StatusCode(StatusCodes.Status500InternalServerError, ex.Message);
            }
        }

        /// <summary>
        /// Get a dimension from a dataset.
        /// </summary>
        /// <remarks>Obtain a dimension from this dataset.</remarks>
        /// <param name="id">Id of the dataset.</param>
        /// <param name="name">Name of the dimension.</param>
        /// <returns>A dataset dimension.</returns>
        [HttpGet("{id}/dimensions/{name}")]
        [ProducesResponseType(StatusCodes.Status200OK)]
        [ProducesResponseType(StatusCodes.Status400BadRequest)]
        [ProducesResponseType(StatusCodes.Status403Forbidden)]
        [ProducesResponseType(StatusCodes.Status404NotFound)]
        public async Task<ActionResult<Dimension>> GetDimensionForDatasetAsync(string id, string name) {
            var dimension = await _dimensions.GetAsync(id, name);
            if(dimension == null) return NotFound();
            else return Ok(dimension);
        }

        /// <summary>
        /// Assign a dimension to this dataset.
        /// </summary>
        /// <remarks>Create or update a dimension.</remarks>
        /// <param name="id">Id of the dataset.</param>
        /// <param name="name">Name of the dimension (unique within dataset).</param>
        /// <param name="dimension">Object representing the dimension.</param>
        /// <returns>Object representing the dimension.</returns>
        [HttpPut("{id}/dimensions/{name}")]
        [ProducesResponseType(StatusCodes.Status200OK)]
        [ProducesResponseType(StatusCodes.Status400BadRequest)]
        [ProducesResponseType(StatusCodes.Status403Forbidden)]
        [ProducesResponseType(StatusCodes.Status409Conflict)]
        [ProducesResponseType(StatusCodes.Status500InternalServerError)]
        public async Task<ActionResult<Dimension>> PutDimensionByNameAsync(string id, string name, Dimension dimension) {
            if(dimension.Name != name) return BadRequest("Resource and dimension name mismatch.");

            try {
                // Add the dimension to the dataset.
                var result = await _dimensions.AddAsync(id, dimension);

                // Return the new dimension as it now stands.
                return Ok(result);
            }
            catch(Exception ex) {
                if(ex is UnauthorizedAccessException) return Forbid(ex.Message);
                else return StatusCode(StatusCodes.Status500InternalServerError, ex.Message);
            }
        }

        /// <summary>
        /// Delete a dataset dimension.
        /// </summary>
        /// <remarks>Delete this dimension from the dataset.</remarks>
        /// <param name="id">Id of the dataset.</param>
        /// <param name="name">Unique name of the dimension.</param>
        [HttpDelete("{id}/dimensions/{name}")]
        [ProducesResponseType(StatusCodes.Status204NoContent)]
        [ProducesResponseType(StatusCodes.Status400BadRequest)]
        [ProducesResponseType(StatusCodes.Status403Forbidden)]
        [ProducesResponseType(StatusCodes.Status409Conflict)]
        [ProducesResponseType(StatusCodes.Status500InternalServerError)]
        public async Task<ActionResult> DeleteDimensionByIdAsync(string id, string name) {
            try {
                // Delete the dimension.
                if(!await _dimensions.DeleteAsync(id, name)) return Conflict();
                else return NoContent(); // Success.
            }
            catch(Exception ex) {
                if(ex is UnauthorizedAccessException) return Forbid(ex.Message);
                else return StatusCode(StatusCodes.Status500InternalServerError, ex.Message);
            }
        }

        /// <summary>
        /// Obtain observations from the dataset.
        /// </summary>
        /// <remarks>Observation data values for a dataset are retrieved at this endpoint.</remarks>
        /// <param name="id">Id of the dataset.</param>
        /// <param name="q">Query using Lucene syntax (e.g. `dimensions.geography:E09000001 AND dimensions.age:>21`).</param>
        /// <returns>Data observations.</returns>
        [HttpGet("{id}/values")]
        [ProducesResponseType(StatusCodes.Status200OK)]
        [ProducesResponseType(StatusCodes.Status400BadRequest)]
        [ProducesResponseType(StatusCodes.Status403Forbidden)]
        [ProducesResponseType(StatusCodes.Status404NotFound)]
        [ProducesResponseType(StatusCodes.Status429TooManyRequests)]
        public async Task<ActionResult<RowMajorObservations>> GetObservationsForDatasetAsync(string id, [FromQuery(Name = "q")] string q) {
            QueryFilterOptions options = new QueryFilterOptions() {
                Query = { Value = q, Syntax = Syntax.Lucene }
            };

            var observations = await _observations.GetAllAsync(id, options);
            if(observations == null) return NotFound();
            else return Ok(observations);
        }

        /// <summary>
        /// Append observation values into this dataset.
        /// </summary>
        /// <remarks>Append observation values (using row-major order) into this dataset, will overwrite if a value exists already.</remarks>
        /// <param name="id">Id of the dataset.</param>
        /// <param name="observations">Observation values using row-major order.</param>
        [HttpPost("{id}/values")]
        [ProducesResponseType(StatusCodes.Status200OK)]
        [ProducesResponseType(StatusCodes.Status400BadRequest)]
        [ProducesResponseType(StatusCodes.Status403Forbidden)]
        [ProducesResponseType(StatusCodes.Status404NotFound)]
        public async Task<ActionResult> PostObservationsForDatasetAsync(string id, RowMajorObservations observations) {
            try {
                // Check dataset exists.
                if(await _datasets.GetAsync(id) == null) return NotFound();

                // Add the observation to the dataset.
                await _observations.AddAsync(id, observations);
                
                return Ok();
            }
            catch(Exception ex) {
                if(ex is UnauthorizedAccessException) return Forbid(ex.Message);
                else if(ex is FormatException) return BadRequest(ex.Message);
                else return StatusCode(StatusCodes.Status500InternalServerError, ex.Message);
            }
        }

        /// <summary>
        /// Replace all observation values.
        /// </summary>
        /// <remarks>Replace all observation values in this dataset (any existing data values not in this set are deleted).</remarks>
        /// <param name="id">Id of the dataset.</param>
        /// <param name="observations">Observation values using row-major order.</param>
        [HttpPut("{id}/values")]
        [ProducesResponseType(StatusCodes.Status200OK)]
        [ProducesResponseType(StatusCodes.Status400BadRequest)]
        [ProducesResponseType(StatusCodes.Status403Forbidden)]
        [ProducesResponseType(StatusCodes.Status409Conflict)]
        [ProducesResponseType(StatusCodes.Status404NotFound)]
        public async Task<ActionResult> PutObservationsForDatasetAsync(string id, RowMajorObservations observations) {
            if(observations == null) return BadRequest("No observations specified.");
            if(observations.Dataset != id) return BadRequest("Resource ID and dataset ID in observation mismatched.");

            
            try {
                // Check dataset exists.
                if(await _datasets.GetAsync(id) == null) return NotFound();

                // Delete all existing observations.
                if(!await _observations.DeleteAsync(id)) return Conflict();

                // Add the observations to the dataset.
                await _observations.AddAsync(id, observations);
                
                return Ok();
            }
            catch(Exception ex) {
                if(ex is UnauthorizedAccessException) return Forbid(ex.Message);
                else if(ex is FormatException) return BadRequest(ex.Message);
                else return StatusCode(StatusCodes.Status500InternalServerError, ex.Message);
            }
        }

        /// <summary>
        /// Delete observations.
        /// </summary>
        /// <remarks>Remove all observations from this dataset.</remarks>
        /// <param name="id">Id of the dataset.</param>
        [HttpDelete("{id}/values")]
        [ProducesResponseType(StatusCodes.Status200OK)]
        [ProducesResponseType(StatusCodes.Status403Forbidden)]
        [ProducesResponseType(StatusCodes.Status409Conflict)]
        [ProducesResponseType(StatusCodes.Status404NotFound)]
        public async Task<ActionResult> DeleteObservationsForDatasetAsync(string id) {
            try {
                // Check dataset exists.
                if(await _datasets.GetAsync(id) == null) return NotFound();

                // Delete all existing observations.
                if(!await _observations.DeleteAsync(id)) return Conflict();                
                else return Ok();
            }
            catch(Exception ex) {
                if(ex is UnauthorizedAccessException) return Forbid(ex.Message);
                else return StatusCode(StatusCodes.Status500InternalServerError, ex.Message);
            }
        }


        /// <summary>
        /// Get units from a dataset.
        /// </summary>
        /// <remarks>Obtain units from this dataset.</remarks>
        /// <param name="id">Id of the dataset.</param>
        /// <param name="q">Query using Lucene syntax (e.g. `label:Household`).</param>
        /// <returns>A list of all dataset units.</returns>
        [HttpGet("{id}/units")]
        [ProducesResponseType(StatusCodes.Status200OK)]
        [ProducesResponseType(StatusCodes.Status400BadRequest)]
        public async Task<ActionResult<IEnumerable<Unit>>> GetUnitsForDatasetAsync(string id, [FromQuery(Name = "q")] string q) {
            QueryFilterOptions options = new QueryFilterOptions() {
                Query = { Value = q, Syntax = Syntax.Lucene }
            };
            
            return Ok(await _units.GetAllAsync(id, options));
        }

        /// <summary>
        /// Get a unit from a dataset.
        /// </summary>
        /// <remarks>Obtain a unit from this dataset.</remarks>
        /// <param name="id">Id of the dataset.</param>
        /// <param name="unitId">Id of the unit.</param>
        /// <returns>A dataset unit.</returns>
        [HttpGet("{id}/units/{unitId}")]
        [ProducesResponseType(StatusCodes.Status200OK)]
        [ProducesResponseType(StatusCodes.Status404NotFound)]
        public async Task<ActionResult<Unit>> GetUnitForDatasetAsync(string id, int unitId) {
            var unit = await _units.GetAsync(id, unitId);
            if(unit == null) return NotFound();
            else return Ok(unit);
        }

        /// <summary>
        /// Assign a unit to this dataset.
        /// </summary>
        /// <remarks>Create or update a unit.</remarks>
        /// <param name="id">Id of the dataset.</param>
        /// <param name="unitId">Id of unit used by observations in this dataset.</param>
        /// <param name="unit">Object representing the unit.</param>
        /// <returns>Object representing the unit.</returns>
        [HttpPut("{id}/units/{unitId}")]
        [ProducesResponseType(StatusCodes.Status200OK)]
        [ProducesResponseType(StatusCodes.Status400BadRequest)]
        [ProducesResponseType(StatusCodes.Status403Forbidden)]
        [ProducesResponseType(StatusCodes.Status409Conflict)]
        [ProducesResponseType(StatusCodes.Status500InternalServerError)]
        public async Task<ActionResult<Unit>> PutUnitByUnitIdAsync(string id, int unitId, Unit unit) {
            if(unit.Id != unitId) return BadRequest("Resource and unit Id mismatch.");

            try {
                // Add the unit to the dataset.
                var result = await _units.AddAsync(id, unit);

                // Return the new unit as it now stands.
                return Ok(result);
            }
            catch(Exception ex) {
                if(ex is UnauthorizedAccessException) return Forbid(ex.Message);
                else return StatusCode(StatusCodes.Status500InternalServerError, ex.Message);
            }
        }

        /// <summary>
        /// Delete a dataset unit.
        /// </summary>
        /// <remarks>Delete this unit from the dataset.</remarks>
        /// <param name="id">Id of the dataset.</param>
        /// <param name="unitId">Unique Id of the unit.</param>
        [HttpDelete("{id}/units/{unitId}")]
        [ProducesResponseType(StatusCodes.Status204NoContent)]
        [ProducesResponseType(StatusCodes.Status400BadRequest)]
        [ProducesResponseType(StatusCodes.Status403Forbidden)]
        [ProducesResponseType(StatusCodes.Status409Conflict)]
        [ProducesResponseType(StatusCodes.Status500InternalServerError)]
        public async Task<ActionResult> DeleteUnitByIdAsync(string id, int unitId) {
            try {
                // Delete the unit.
                if(!await _units.DeleteAsync(id, unitId)) return Conflict();
                else return NoContent(); // Success.
            }
            catch(Exception ex) {
                if(ex is UnauthorizedAccessException) return Forbid(ex.Message);
                else return StatusCode(StatusCodes.Status500InternalServerError, ex.Message);
            }
        }

        /// <summary>
        /// Get observation status codes.
        /// </summary>
        /// <remarks>Obtain all possible observation status codes from this dataset.</remarks>
        /// <param name="id">Id of the dataset.</param>
        /// <param name="q">Query using Lucene syntax (e.g. `message:Confidential`).</param>
        /// <returns>A list of all possible observation status codes.</returns>
        [HttpGet("{id}/status-codes")]
        [ProducesResponseType(StatusCodes.Status200OK)]
        [ProducesResponseType(StatusCodes.Status400BadRequest)]
        public async Task<ActionResult<IEnumerable<Status>>> GetStatusForDatasetAsync(string id, [FromQuery(Name = "q")] string q) {
            QueryFilterOptions options = new QueryFilterOptions() {
                Query = { Value = q, Syntax = Syntax.Lucene }
            };
            
            return Ok(await _status.GetAllAsync(id, options));
        }

        /// <summary>
        /// Get a observation status code from a dataset.
        /// </summary>
        /// <remarks>Obtain a observation status code from this dataset.</remarks>
        /// <param name="id">Id of the dataset.</param>
        /// <param name="statusId">Id of the status.</param>
        /// <returns>A dataset unit.</returns>
        [HttpGet("{id}/status-codes/{statusId}")]
        [ProducesResponseType(StatusCodes.Status200OK)]
        [ProducesResponseType(StatusCodes.Status404NotFound)]
        public async Task<ActionResult<Status>> GetStatusForDatasetAsync(string id, int statusId) {
            var status = await _status.GetAsync(id, statusId);
            if(status == null) return NotFound();
            else return Ok(status);
        }

        /// <summary>
        /// Assign a status for observations.
        /// </summary>
        /// <remarks>Create or update a status code for use on observations in this dataset.</remarks>
        /// <param name="id">Id of the dataset.</param>
        /// <param name="statusId">Id of status code used by observations in this dataset.</param>
        /// <param name="status">Object representing the status.</param>
        /// <returns>Object representing the status.</returns>
        [HttpPut("{id}/status-codes/{statusId}")]
        [ProducesResponseType(StatusCodes.Status200OK)]
        [ProducesResponseType(StatusCodes.Status400BadRequest)]
        [ProducesResponseType(StatusCodes.Status403Forbidden)]
        [ProducesResponseType(StatusCodes.Status409Conflict)]
        [ProducesResponseType(StatusCodes.Status500InternalServerError)]
        public async Task<ActionResult<Status>> PutStatusByStatusIdAsync(string id, int statusId, Status status) {
            if(status.Id != statusId) return BadRequest("Resource and status Id mismatch.");

            try {
                // Add the status to the dataset.
                var result = await _status.AddAsync(id, status);

                // Return the new status as it now stands.
                return Ok(result);
            }
            catch(Exception ex) {
                if(ex is UnauthorizedAccessException) return Forbid(ex.Message);
                else return StatusCode(StatusCodes.Status500InternalServerError, ex.Message);
            }
        }

        /// <summary>
        /// Delete a dataset observation status code.
        /// </summary>
        /// <remarks>Delete this status code from the dataset.</remarks>
        /// <param name="id">Id of the dataset.</param>
        /// <param name="statusId">Unique Id of the status code.</param>
        [HttpDelete("{id}/status-codes/{statusId}")]
        [ProducesResponseType(StatusCodes.Status204NoContent)]
        [ProducesResponseType(StatusCodes.Status400BadRequest)]
        [ProducesResponseType(StatusCodes.Status403Forbidden)]
        [ProducesResponseType(StatusCodes.Status409Conflict)]
        [ProducesResponseType(StatusCodes.Status500InternalServerError)]
        public async Task<ActionResult> DeleteStatusByIdAsync(string id, int statusId) {
            try {
                // Delete the status.
                if(!await _status.DeleteAsync(id, statusId)) return Conflict();
                else return NoContent(); // Success.
            }
            catch(Exception ex) {
                if(ex is UnauthorizedAccessException) return Forbid(ex.Message);
                else return StatusCode(StatusCodes.Status500InternalServerError, ex.Message);
            }
        }
    }
}
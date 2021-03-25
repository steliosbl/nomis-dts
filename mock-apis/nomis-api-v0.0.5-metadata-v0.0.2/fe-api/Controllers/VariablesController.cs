using System;
using System.Collections.Generic;
using System.Threading.Tasks;

using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Logging;

using Nomis.Interfaces.Variables.Models;
using Nomis.Interfaces.Variables.Repository;
using Nomis.Interfaces.Core.Models;

namespace fe_api.Controllers
{
    [ApiController]
    [Route("[controller]")]
    public class VariablesController : ControllerBase
    {
        private readonly ILogger<VariablesController> _logger;
        private readonly IVariableStore _variables;
        private readonly ICategoryStore _categories;
        private readonly ICategoryTypeStore _categorytypes;

        public VariablesController(  ILogger<VariablesController> logger,
                                    IVariableStore variables,
                                    ICategoryStore categories,
                                    ICategoryTypeStore categoryTypes)
        {
            _logger = logger;
            _variables = variables;
            _categories = categories;
            _categorytypes = categoryTypes;
        }

        /// <summary>
        /// Get a list of all variables.
        /// </summary>
        /// <remarks>Provides access to the complete list of variables.</remarks>
        /// <param name="q">Query using Lucene syntax (e.g. `label:Age OR label:Gender`).</param>
        /// <returns>A list of variables.</returns>
        [HttpGet]
        [ProducesResponseType(StatusCodes.Status200OK)]
        [ProducesResponseType(StatusCodes.Status400BadRequest)]
        public async Task<ActionResult<IEnumerable<Variable>>> GetAllDatasets([FromQuery(Name = "q")] string q)
        {
            QueryFilterOptions options = new QueryFilterOptions() {
                Query = { Value = q, Syntax = Syntax.Lucene }
            };

            return Ok(await _variables.GetAllAsync(options));
        }

        /// <summary>
        /// Get variable definitiion.
        /// </summary>
        /// <remarks>Obtain a specific variable.</remarks>
        /// <param name="name">Unique name of the variable.</param>
        /// <param name="view">The view context to apply to the variable.</param>
        /// <returns>Object representing the variable.</returns>
        [HttpGet("{name}")]
        [ProducesResponseType(StatusCodes.Status200OK)]
        [ProducesResponseType(StatusCodes.Status400BadRequest)]
        [ProducesResponseType(StatusCodes.Status403Forbidden)]
        [ProducesResponseType(StatusCodes.Status404NotFound)]
        public async Task<ActionResult<Variable>> GetVariableByName(string name, [FromQuery(Name = "view")]string view = null) {
            var dataset = await _variables.GetAsync(name, view);
            if(dataset == null) return NotFound();
            else return Ok(dataset);
        }

        /// <summary>
        /// Update/create a variable.
        /// </summary>
        /// <remarks>Update/create a variable.</remarks>
        /// <param name="name">Unique name of the variable.</param>
        /// <param name="variable">Object representing the variable.</param>
        /// <returns>Dataset details.</returns>
        [HttpPut("{name}")]
        [ProducesResponseType(StatusCodes.Status200OK)]
        [ProducesResponseType(StatusCodes.Status400BadRequest)]
        [ProducesResponseType(StatusCodes.Status403Forbidden)]
        [ProducesResponseType(StatusCodes.Status409Conflict)]
        [ProducesResponseType(StatusCodes.Status500InternalServerError)]
        public async Task<ActionResult<Variable>> PutVariableById(string name, Variable variable) {
            if(name != variable.Name) return BadRequest("Resource and variable name mismatched");

            try {
                Variable var;

                if(await _variables.GetAsync(name, null) != null) {
                    var = await _variables.UpdateAsync(variable);
                }
                else var = await _variables.AddAsync(variable);

                if(var == null) return Conflict();
                else return Ok(var);
            }
            catch(Exception ex) {
                if(ex is UnauthorizedAccessException) return Forbid(ex.Message);
                else return StatusCode(StatusCodes.Status500InternalServerError, ex.Message);
            }
        }

        /// <summary>
        /// Update a variable.
        /// </summary>
        /// <remarks>Update a variable.</remarks>
        /// <param name="name">Unique name of the variable.</param>
        /// <param name="variable">Partial object containing changed variable properties.</param>
        /// <returns>Variable object.</returns>
        [HttpPatch("{name}")]
        [ProducesResponseType(StatusCodes.Status200OK)]
        [ProducesResponseType(StatusCodes.Status400BadRequest)]
        [ProducesResponseType(StatusCodes.Status403Forbidden)]
        [ProducesResponseType(StatusCodes.Status500InternalServerError)]
        public async Task<ActionResult<Variable>> PatchVariableByName(string name, Variable variable) {
            if(name != variable.Name) return BadRequest("Resource and variable name mismatched");

            try {
                var updated = await _variables.UpdateAsync(variable);
                return Ok(updated);
            }
            catch(Exception ex) {
                if(ex is UnauthorizedAccessException) return Forbid(ex.Message);
                else return StatusCode(StatusCodes.Status500InternalServerError, ex.Message);
            }
        }

        /// <summary>
        /// Delete a variable.
        /// </summary>
        /// <remarks>Delete this variable.</remarks>
        /// <param name="name">Unique name of the variable.</param>
        [HttpDelete("{name}")]
        [ProducesResponseType(StatusCodes.Status204NoContent)]
        [ProducesResponseType(StatusCodes.Status400BadRequest)]
        [ProducesResponseType(StatusCodes.Status403Forbidden)]
        [ProducesResponseType(StatusCodes.Status409Conflict)]
        [ProducesResponseType(StatusCodes.Status500InternalServerError)]
        public async Task<ActionResult> DeleteVariableByName(string name) {
            try {
                // Delete the unit.
                if(!await _variables.DeleteAsync(name)) return Conflict();
                else return NoContent(); // Success.
            }
            catch(Exception ex) {
                if(ex is UnauthorizedAccessException) return Forbid(ex.Message);
                else return StatusCode(StatusCodes.Status500InternalServerError, ex.Message);
            }
        }

        /// <summary>
        /// List categories available from a variable.
        /// </summary>
        /// <remarks>Obtain a list of all categories of this variable.</remarks>
        /// <param name="name">Name of the variable.</param>
        /// <param name="view">The view context to apply to the variable.</param>
        /// <param name="q">Query using Lucene syntax (e.g. `title:Male OR title:Female`).</param>
        /// <returns>A list of categories.</returns>
        [HttpGet("{name}/categories")]
        [ProducesResponseType(StatusCodes.Status200OK)]
        [ProducesResponseType(StatusCodes.Status400BadRequest)]
        [ProducesResponseType(StatusCodes.Status403Forbidden)]
        [ProducesResponseType(StatusCodes.Status404NotFound)]
        public async Task<ActionResult<IEnumerable<Category>>> GetCategoriesForVariable(string name, [FromQuery(Name = "view")] string view, [FromQuery(Name = "q")] string q) {
            QueryFilterOptions options = new QueryFilterOptions() {
                Query = { Value = q, Syntax = Syntax.Lucene }
            };

            var categories = await _categories.GetAllAsync(name, view, options);
            if(categories == null) return NotFound();
            else return Ok(categories);
        }

        /// <summary>
        /// Update variable categories.
        /// </summary>
        /// <remarks>Add categories to variable (any categories not in this set are deleted from the variable).</remarks>
        /// <param name="name">Unique name of the variable.</param>
        /// <param name="categories">List of objects representing categories.</param>
        /// <returns>List of categories.</returns>
        [HttpPut("{name}/categories")]
        [ProducesResponseType(StatusCodes.Status200OK)]
        [ProducesResponseType(StatusCodes.Status400BadRequest)]
        [ProducesResponseType(StatusCodes.Status403Forbidden)]
        [ProducesResponseType(StatusCodes.Status404NotFound)]
        [ProducesResponseType(StatusCodes.Status409Conflict)]
        [ProducesResponseType(StatusCodes.Status500InternalServerError)]
        public async Task<ActionResult<IEnumerable<Category>>> PutCategoriesByVariableName(string name, Category[] categories) {
            var variable = await _variables.GetAsync(name, null);
            if(variable == null) return NotFound();

            try {
                // Remove existing categories in variable before adding new.
                if(!await _categories.DeleteAllAsync(name)) return Conflict();
                
                List<Category> results = new List<Category>();

                foreach(Category category in categories) {
                    var result = await _categories.AddAsync(name, category);
                    results.Add(result);
                }

                return Ok(results);
            }
            catch(Exception ex) {
                if(ex is UnauthorizedAccessException) return Forbid(ex.Message);
                else return StatusCode(StatusCodes.Status500InternalServerError, ex.Message);
            }
        }

        /// <summary>
        /// Delete all categories.
        /// </summary>
        /// <remarks>Delete all categories from a variable.</remarks>
        /// <param name="name">Unique name of the variable.</param>
        [HttpDelete("{name}/categories")]
        [ProducesResponseType(StatusCodes.Status204NoContent)]
        [ProducesResponseType(StatusCodes.Status400BadRequest)]
        [ProducesResponseType(StatusCodes.Status403Forbidden)]
        [ProducesResponseType(StatusCodes.Status409Conflict)]
        [ProducesResponseType(StatusCodes.Status500InternalServerError)]
        public async Task<ActionResult> DeleteCategoriesByVariableName(string name) {
            try {
                if(!await _categories.DeleteAllAsync(name)) return Conflict();

                // Return success.
                return NoContent();
            }
            catch(Exception ex) {
                if(ex is UnauthorizedAccessException) return Forbid(ex.Message);
                else return StatusCode(StatusCodes.Status500InternalServerError, ex.Message);
            }
        }

        /// <summary>
        /// Get a category from a variable.
        /// </summary>
        /// <remarks>Obtain a dimension from this variable.</remarks>
        /// <param name="name">Name of the variable.</param>
        /// <param name="code">Unique code of the category.</param>
        /// <param name="view">The view context to apply to the category.</param>
        /// <returns>A variable category.</returns>
        [HttpGet("{name}/categories/{code}")]
        [ProducesResponseType(StatusCodes.Status200OK)]
        [ProducesResponseType(StatusCodes.Status400BadRequest)]
        [ProducesResponseType(StatusCodes.Status403Forbidden)]
        [ProducesResponseType(StatusCodes.Status404NotFound)]
        public async Task<ActionResult<Category>> GetCategoryForVariable(string name, string code, [FromQuery(Name="view")]string view) {
            var category = await _categories.GetAsync(name, code, view);
            if(category == null) return NotFound();
            else return Ok(category);
        }

        /// <summary>
        /// Create/update a category.
        /// </summary>
        /// <remarks>Create/update a category in an existing variable.</remarks>
        /// <param name="name">Unique name of the variable.</param>
        /// <param name="code">Unique code of the category.</param>
        /// <param name="category">Object representing the category.</param>
        /// <returns>Object representing newly created category.</returns>
        [HttpPut("{name}/categories/{code}")]
        [ProducesResponseType(StatusCodes.Status200OK)]
        [ProducesResponseType(StatusCodes.Status400BadRequest)]
        [ProducesResponseType(StatusCodes.Status403Forbidden)]
        [ProducesResponseType(StatusCodes.Status404NotFound)]
        [ProducesResponseType(StatusCodes.Status500InternalServerError)]
        public async Task<ActionResult<Category>> PutCategoryByVariableName(string name, string code, Category category) {
            if(code != category.Code) return BadRequest("Resource and category code mismatched");

            var variable = await _variables.GetAsync(name, null);
            if(variable == null) return NotFound();

            try {
                if(!await _categories.DeleteAsync(name, category.Code)) return Conflict();

                var result = await _categories.AddAsync(name, category);

                if(result == null) return Conflict();
                else return Ok(result);
            }
            catch(Exception ex) {
                if(ex is UnauthorizedAccessException) return Forbid(ex.Message);
                else return StatusCode(StatusCodes.Status500InternalServerError, ex.Message);
            }
        }

        /// <summary>
        /// Partial category update.
        /// </summary>
        /// <remarks>Partially update an existing category.</remarks>
        /// <param name="name">Unique name of the variable.</param>
        /// <param name="code">Unique code of the category.</param>
        /// <param name="category">Partial object representing the category.</param>
        /// <returns>Object representing modified category.</returns>
        [HttpPatch("{name}/categories/{code}")]
        [ProducesResponseType(StatusCodes.Status200OK)]
        [ProducesResponseType(StatusCodes.Status400BadRequest)]
        [ProducesResponseType(StatusCodes.Status403Forbidden)]
        [ProducesResponseType(StatusCodes.Status404NotFound)]
        [ProducesResponseType(StatusCodes.Status500InternalServerError)]
        public async Task<ActionResult<Category>> PatchCategoryByVariableName(string name, string code, Category category) {
            if(code != category.Code) return BadRequest("Resource and category code mismatched");

            var variable = await _variables.GetAsync(name, null);
            if(variable == null) return NotFound();

            try {
                var result = await _categories.UpdateAsync(name, category);

                if(result == null) return Conflict();
                return Ok(result);
            }
            catch(Exception ex) {
                if(ex is UnauthorizedAccessException) return Forbid(ex.Message);
                else return StatusCode(StatusCodes.Status500InternalServerError, ex.Message);
            }
        }
        
        /// <summary>
        /// Delete a category.
        /// </summary>
        /// <remarks>Delete a category from a variable.</remarks>
        /// <param name="name">Unique name of the variable.</param>
        /// <param name="code">Unique code of the category.</param>
        [HttpDelete("{name}/categories/{code}")]
        [ProducesResponseType(StatusCodes.Status204NoContent)]
        [ProducesResponseType(StatusCodes.Status400BadRequest)]
        [ProducesResponseType(StatusCodes.Status403Forbidden)]
        [ProducesResponseType(StatusCodes.Status404NotFound)]
        [ProducesResponseType(StatusCodes.Status409Conflict)]
        [ProducesResponseType(StatusCodes.Status500InternalServerError)]
        public async Task<ActionResult> DeleteCategoryByVariableName(string name, string code) {
            try {
                var category = await _categories.GetAsync(name, code, null);
                if(category == null) return NotFound();

                if(await _categories.DeleteAsync(name, code)) return NoContent(); // Success.
                else return Conflict();
            }
            catch(Exception ex) {
                if(ex is UnauthorizedAccessException) return Forbid(ex.Message);
                else return StatusCode(StatusCodes.Status500InternalServerError, ex.Message);
            }
        }

        /// <summary>
        /// Lists root variable categories.
        /// </summary>
        /// <remarks>Obtain root variable categories (those without ancestors).</remarks>
        /// <param name="name">Name of the variable.</param>
        /// <param name="view">The view context to apply.</param>
        /// <param name="typeId">The type Id to filter results.</param>
        /// <param name="hierarchyId">The hierarchy Id for context. Root categories will be limited to only those where they are mentioned as an ancestor within the context of this hierarchy.</param>
        /// <returns>List of root variable categories.</returns>
        [HttpGet("{name}/root-categories")]
        [ProducesResponseType(StatusCodes.Status200OK)]
        [ProducesResponseType(StatusCodes.Status400BadRequest)]
        [ProducesResponseType(StatusCodes.Status403Forbidden)]
        [ProducesResponseType(StatusCodes.Status404NotFound)]
        public async Task<ActionResult<IEnumerable<Category>>> GetCategoryRootForVariable(
            string name,
            [FromQuery(Name="view")]string view,
            [FromQuery(Name="typeId")]string typeId,
            [FromQuery(Name="hierarchyId")]string hierarchyId
            ) {
                var category = await _categories.GetRootCategoriesAsync(name, view, typeId, hierarchyId, null);
                if(category == null) return NotFound();
                else return Ok(category);
            }

        /// <summary>
        /// Lists immediate, or specific ancestors of a variable category.
        /// </summary>
        /// <remarks>Obtain the immediate, or specific ancestors of a variable category.</remarks>
        /// <param name="name">Name of the variable.</param>
        /// <param name="code">Unique code of the category.</param>
        /// <param name="view">The view context to apply to the category.</param>
        /// <param name="typeId">The type Id to filter results.</param>
        /// <param name="hierarchyId">The hierarchy Id for context.</param>
        /// <returns>List of variable categories.</returns>
        [HttpGet("{name}/categories/{code}/ancestors")]
        [ProducesResponseType(StatusCodes.Status200OK)]
        [ProducesResponseType(StatusCodes.Status400BadRequest)]
        [ProducesResponseType(StatusCodes.Status403Forbidden)]
        [ProducesResponseType(StatusCodes.Status404NotFound)]
        public async Task<ActionResult<IEnumerable<Category>>> GetCategoryAncestorsForVariable(
            string name,
            string code,
            [FromQuery(Name="view")]string view,
            [FromQuery(Name="typeId")]string typeId,
            [FromQuery(Name="hierarchyId")]string hierarchyId
            ) {
                var category = await _categories.GetCategoryAncestorsAsync(name, code, view, typeId, hierarchyId, null);
                if(category == null) return NotFound();
                else return Ok(category);
            }

        /// <summary>
        /// Lists immediate, or specific descendants of a variable category.
        /// </summary>
        /// <remarks>Obtain the immediate, or specific descendants of a variable category.</remarks>
        /// <param name="name">Name of the variable.</param>
        /// <param name="code">Unique code of the category.</param>
        /// <param name="view">The view context to apply to the category.</param>
        /// <param name="typeId">The type Id to filter results.</param>
        /// <param name="hierarchyId">The hierarchy Id for context.</param>
        /// <returns>List of variable categories.</returns>
        [HttpGet("{name}/categories/{code}/descendants")]
        [ProducesResponseType(StatusCodes.Status200OK)]
        [ProducesResponseType(StatusCodes.Status400BadRequest)]
        [ProducesResponseType(StatusCodes.Status403Forbidden)]
        [ProducesResponseType(StatusCodes.Status404NotFound)]
        public async Task<ActionResult<IEnumerable<Category>>> GetCategoryDescendantsForVariable(
            string name,
            string code,
            [FromQuery(Name="view")]string view,
            [FromQuery(Name="typeId")]string typeId,
            [FromQuery(Name="hierarchyId")]string hierarchyId
            ) {
                var category = await _categories.GetCategoryDescendantsAsync(name, code, view, typeId, hierarchyId, null);
                if(category == null) return NotFound();
                else return Ok(category);
            }   

        /// <summary>
        /// List category types available from a variable.
        /// </summary>
        /// <remarks>Obtain a list of all category types of this variable.</remarks>
        /// <param name="name">Name of the variable.</param>
        /// <param name="view">The view context to apply to the category types.</param>
        /// <param name="q">Query using Lucene syntax (e.g. `title:Region`).</param>
        /// <returns>A list of category types.</returns>
        [HttpGet("{name}/types")]
        [ProducesResponseType(StatusCodes.Status200OK)]
        [ProducesResponseType(StatusCodes.Status400BadRequest)]
        [ProducesResponseType(StatusCodes.Status403Forbidden)]
        [ProducesResponseType(StatusCodes.Status404NotFound)]
        public async Task<ActionResult<IEnumerable<CategoryType>>> GetCategoryTypesForVariable(string name, [FromQuery(Name = "view")] string view, [FromQuery(Name = "q")] string q) {
            QueryFilterOptions options = new QueryFilterOptions() {
                Query = { Value = q, Syntax = Syntax.Lucene }
            };

            var categoryTypes = await _categorytypes.GetAllAsync(name, view, options);
            if(categoryTypes == null) return NotFound();
            else return Ok(categoryTypes);
        }

        /// <summary>
        /// Create/update category types.
        /// </summary>
        /// <remarks>Create or update category types for this variable (all existing types are deleted).</remarks>
        /// <param name="name">Name of the variable.</param>
        /// <param name="types">List of objects representing the category types.</param>
        /// <returns>Object representing the type.</returns>
        [HttpPut("{name}/types")]
        [ProducesResponseType(StatusCodes.Status200OK)]
        [ProducesResponseType(StatusCodes.Status400BadRequest)]
        [ProducesResponseType(StatusCodes.Status403Forbidden)]
        [ProducesResponseType(StatusCodes.Status409Conflict)]
        [ProducesResponseType(StatusCodes.Status500InternalServerError)]
        public async Task<ActionResult<IEnumerable<CategoryType>>> PutTypesByVariableName(string name, CategoryType[] types) {
            try {
                // Delete all existing types
                if(!await _categorytypes.DeleteAllAsync(name)) return Conflict();

                List<CategoryType> results = new List<CategoryType>();

                foreach(CategoryType type in types) {
                    // Add the type to the dataset.
                    var result = await _categorytypes.AddAsync(name, type);
                
                    if(result != null) results.Add(result);
                    else return Conflict();
                }

                // Return the new types as they now stands.
                return Ok(results);
            }
            catch(Exception ex) {
                if(ex is UnauthorizedAccessException) return Forbid(ex.Message);
                else return StatusCode(StatusCodes.Status500InternalServerError, ex.Message);
            }
        }

        /// <summary>
        /// Delete all category types.
        /// </summary>
        /// <remarks>Delete all category types from the variable.</remarks>
        /// <param name="name">Name of the variable.</param>
        [HttpDelete("{name}/types")]
        [ProducesResponseType(StatusCodes.Status204NoContent)]
        [ProducesResponseType(StatusCodes.Status400BadRequest)]
        [ProducesResponseType(StatusCodes.Status403Forbidden)]
        [ProducesResponseType(StatusCodes.Status404NotFound)]
        [ProducesResponseType(StatusCodes.Status409Conflict)]
        [ProducesResponseType(StatusCodes.Status500InternalServerError)]
        public async Task<ActionResult> DeleteTypesByVariableName(string name) {
            try {
                // Check if variable exists.
                var v = await _variables.GetAsync(name, null);
                if(v == null) return NotFound();

                // Delete all the types.
                if(!await _categorytypes.DeleteAllAsync(name)) return Conflict();
                else return NoContent(); // Success.
            }
            catch(Exception ex) {
                if(ex is UnauthorizedAccessException) return Forbid(ex.Message);
                else return StatusCode(StatusCodes.Status500InternalServerError, ex.Message);
            }
        }

        /// <summary>
        /// Get a category type from a variable.
        /// </summary>
        /// <remarks>Obtain a category type from this variable.</remarks>
        /// <param name="name">Name of the variable.</param>
        /// <param name="typeId">Unique Id of the category type.</param>
        /// <param name="view">The view context to apply to the type.</param>
        /// <returns>A variable category.</returns>
        [HttpGet("{name}/types/{typeId}")]
        [ProducesResponseType(StatusCodes.Status200OK)]
        [ProducesResponseType(StatusCodes.Status400BadRequest)]
        [ProducesResponseType(StatusCodes.Status403Forbidden)]
        [ProducesResponseType(StatusCodes.Status404NotFound)]
        public async Task<ActionResult<CategoryType>> GetCategoryTypeForVariable(string name, string typeId, [FromQuery(Name="view")]string view) {
            var categoryType = await _categorytypes.GetAsync(name, typeId, view);
            if(categoryType == null) return NotFound();
            else return Ok(categoryType);
        }

        /// <summary>
        /// Create/update a category type.
        /// </summary>
        /// <remarks>Create or update a type for this variable.</remarks>
        /// <param name="name">Id of the dataset.</param>
        /// <param name="typeId">Id of type.</param>
        /// <param name="type">Object representing the type.</param>
        /// <returns>Object representing the type.</returns>
        [HttpPut("{name}/types/{typeId}")]
        [ProducesResponseType(StatusCodes.Status200OK)]
        [ProducesResponseType(StatusCodes.Status400BadRequest)]
        [ProducesResponseType(StatusCodes.Status403Forbidden)]
        [ProducesResponseType(StatusCodes.Status409Conflict)]
        [ProducesResponseType(StatusCodes.Status500InternalServerError)]
        public async Task<ActionResult<CategoryType>> PutTypeByVariableName(string name, string typeId, CategoryType type) {
            if(type.Id != typeId) return BadRequest("Resource and type Id mismatch.");

            try {
                // Add the unit to the dataset.
                var result = await _categorytypes.AddAsync(name, type);

                // Return the new unit it now stands.
                if(result == null) return Conflict();
                else return Ok(result);
            }
            catch(Exception ex) {
                if(ex is UnauthorizedAccessException) return Forbid(ex.Message);
                else return StatusCode(StatusCodes.Status500InternalServerError, ex.Message);
            }
        }

        /// <summary>
        /// Partial update a category type.
        /// </summary>
        /// <remarks>Partial update of a type for this variable.</remarks>
        /// <param name="name">Name of the variable.</param>
        /// <param name="typeId">Id of type.</param>
        /// <param name="type">Partial object representing the type.</param>
        /// <returns>Object representing the type.</returns>
        [HttpPatch("{name}/types/{typeId}")]
        [ProducesResponseType(StatusCodes.Status200OK)]
        [ProducesResponseType(StatusCodes.Status400BadRequest)]
        [ProducesResponseType(StatusCodes.Status403Forbidden)]
        [ProducesResponseType(StatusCodes.Status409Conflict)]
        [ProducesResponseType(StatusCodes.Status500InternalServerError)]
        public async Task<ActionResult<CategoryType>> PatchTypeByVariableName(string name, string typeId, CategoryType type) {
            if(type.Id != typeId) return BadRequest("Resource and type Id mismatch.");

            try {
                // Add the unit to the dataset.
                var result = await _categorytypes.UpdateAsync(name, type);

                // Return the new unit it now stands.
                if(result == null) return Conflict();
                else return Ok(result);
            }
            catch(Exception ex) {
                if(ex is UnauthorizedAccessException) return Forbid(ex.Message);
                else return StatusCode(StatusCodes.Status500InternalServerError, ex.Message);
            }
        }

        /// <summary>
        /// Delete a category type.
        /// </summary>
        /// <remarks>Delete this category type from the variable.</remarks>
        /// <param name="name">Name of the variable.</param>
        /// <param name="typeId">Unique Id of the category type.</param>
        [HttpDelete("{name}/types/{typeId}")]
        [ProducesResponseType(StatusCodes.Status204NoContent)]
        [ProducesResponseType(StatusCodes.Status400BadRequest)]
        [ProducesResponseType(StatusCodes.Status403Forbidden)]
        [ProducesResponseType(StatusCodes.Status404NotFound)]
        [ProducesResponseType(StatusCodes.Status409Conflict)]
        [ProducesResponseType(StatusCodes.Status500InternalServerError)]
        public async Task<ActionResult> DeleteTypeByVariableName(string name, string typeId) {
            try {
                // See if type exists.
                var t = await _categorytypes.GetAsync(name, typeId, null);
                if(t == null) return NotFound();

                // Delete the unit.
                if(!await _categorytypes.DeleteAsync(name, typeId)) return Conflict();
                else return NoContent(); // Success.
            }
            catch(Exception ex) {
                if(ex is UnauthorizedAccessException) return Forbid(ex.Message);
                else return StatusCode(StatusCodes.Status500InternalServerError, ex.Message);
            }
        }
    }
}

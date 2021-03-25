using System.Collections.Generic;
using System.Threading.Tasks;

using Nomis.Interfaces.Core.Models;
using Nomis.Interfaces.Variables.Models;

namespace Nomis.Interfaces.Variables.Repository {
    public interface ICategoryStore {
        Task<Category> AddAsync(string variableName, Category category);

        Task<Category> UpdateAsync(string variableName, Category category);

        Task<bool> DeleteAsync(string variableName, string code);
        
        Task<bool> DeleteAllAsync(string variableName);

        Task<Category> GetAsync(string variableName, string code, string view);

        Task<List<Category>> GetAllAsync(string variableName, string view, QueryFilterOptions options);

        Task<List<Category>> GetRootCategoriesAsync(string variableName, string view, string typeId, string hierarchyId, QueryFilterOptions options);

        Task<List<Category>> GetCategoryAncestorsAsync(string variableName, string code, string view, string typeId, string hierarchyId, QueryFilterOptions options);

        Task<List<Category>> GetCategoryDescendantsAsync(string variableName, string code, string view, string typeId, string hierarchyId, QueryFilterOptions options);

        
    }
}
using System.Collections.Generic;
using System.Threading.Tasks;

using Nomis.Interfaces.Core.Models;
using Nomis.Interfaces.Variables.Models;

namespace Nomis.Interfaces.Variables.Repository {
    public interface ICategoryTypeStore {
        Task<CategoryType> AddAsync(string variableName, CategoryType type);

        Task<CategoryType> UpdateAsync(string variableName, CategoryType type);

        Task<bool> DeleteAsync(string variableName, string typeId);

        Task<bool> DeleteAllAsync(string variableName);
        
        Task<CategoryType> GetAsync(string variableName, string typeId, string view);

        Task<List<CategoryType>> GetAllAsync(string variableName, string view, QueryFilterOptions options);
    }
}
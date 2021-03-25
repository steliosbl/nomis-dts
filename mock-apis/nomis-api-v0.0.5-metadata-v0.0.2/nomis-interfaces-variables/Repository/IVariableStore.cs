using System.Collections.Generic;
using System.Threading.Tasks;

using Nomis.Interfaces.Core.Models;
using Nomis.Interfaces.Variables.Models;

namespace Nomis.Interfaces.Variables.Repository {
    public interface IVariableStore {
        Task<Variable> AddAsync(Variable variable);

        Task<Variable> UpdateAsync(Variable variable);

        Task<bool> DeleteAsync(string id);
        
        Task<Variable> GetAsync(string id, string view);

        Task<List<Variable>> GetAllAsync(QueryFilterOptions options);
    }
}
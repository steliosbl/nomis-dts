using System.Collections.Generic;
using System.Threading.Tasks;

using Nomis.Interfaces.Datasets.Models;
using Nomis.Interfaces.Core.Models;

namespace Nomis.Interfaces.Datasets.Repository {
    public interface IUnitStore {
        Task<Unit> AddAsync(string datasetId, Unit unit);
        Task<Unit> UpdateAsync(string datasetId, Unit Unit);
        Task<bool> DeleteAsync(string datasetId, int unitId);
        
        Task<Unit> GetAsync(string datasetId, int unitId);
        Task<List<Unit>> GetAllAsync(string datasetId, QueryFilterOptions options);
    }
}
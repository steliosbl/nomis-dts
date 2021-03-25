using System.Collections.Generic;
using System.Threading.Tasks;

using Nomis.Interfaces.Datasets.Models;
using Nomis.Interfaces.Core.Models;

namespace Nomis.Interfaces.Datasets.Repository {
    public interface IObservationStore {
        Task<RowMajorObservations> AddAsync(string datasetId, RowMajorObservations observations);
        Task<bool> DeleteAsync(string datasetId);
        Task<RowMajorObservations> GetAllAsync(string datasetId, QueryFilterOptions options);
    }
}
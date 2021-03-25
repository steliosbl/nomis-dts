using System.Threading.Tasks;
using System.Collections.Generic;

using Nomis.Interfaces.Metadata.Models;

namespace Nomis.Interfaces.Metadata.Repository {
    public interface IRdfNamespaceStore {
        Task<bool> AddAsync(RdfNamespace rdf);
        Task<bool> UpdateAsync(RdfNamespace rdf);
        Task<bool> DeleteAsync(string prefix);

        Task<IEnumerable<RdfNamespace>> GetAllAsync();
        Task<RdfNamespace> GetAsync(string prefix);
    }
}
using System.Collections.Generic;

using Nomis.Interfaces.Datasets.Models;

namespace Nomis.Interfaces.Datasets.Models {
    public class DatabaseInfo {
        public bool IsKey { get; set; } = false;
        public int Index { get; set; }
        public string DefaultView { get; set; }
        public List<Discontinuity> Discontinuities { get; set; }
    }
}
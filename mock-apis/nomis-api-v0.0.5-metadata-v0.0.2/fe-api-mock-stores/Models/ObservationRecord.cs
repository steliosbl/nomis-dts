using System.Collections.Generic;

using Nomis.Interfaces.Datasets.Models;

namespace Nomis.MockStores.Models {
    public class ObservationRecord {
        public List<DimensionMapping> Dimensions { get; set; }
        public ObservationValue Observation { get; set; }
    }
}
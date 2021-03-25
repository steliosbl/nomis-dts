using System.Collections.Generic;

using Nomis.Interfaces.Datasets.Models;

namespace Nomis.MockStores.Models {
    public class ObservationValue {
        public double Value { get; set; } = 0;
        public int StatusId { get; set; }

        public ObservationValue() { }
    }
}
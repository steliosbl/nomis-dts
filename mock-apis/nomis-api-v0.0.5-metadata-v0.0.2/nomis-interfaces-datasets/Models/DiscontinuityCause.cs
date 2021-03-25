using System.Collections.Generic;

namespace Nomis.Interfaces.Datasets.Models {
    public class DiscontinuityCause {
        public string Variable { get; set; }
        public List<string> Categories { get; set; }

        public DiscontinuityCause() { }
    }
}
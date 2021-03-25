namespace Nomis.Interfaces.Datasets.Models {
    public class Discontinuity {
        public string View { get; set; }
        public DiscontinuityCause CausedBy { get; set; }
        public Discontinuity() { }
    }
}
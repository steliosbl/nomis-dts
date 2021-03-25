using System;
using System.Collections.Generic;

namespace Nomis.Interfaces.Datasets.Models {
    public class RowMajorObservations {
        /// <summary>ID of dataset to which values relate.</summary>
        public string Dataset { get; set; }

        /// <summary>A list of dimension IDs for each of the lists of codes in the `Codes` property.</summary>
        public List<string> Dimensions { get; set; }

        /// <summary>A list of category codes for each of observations in row-major order.</summary>
        public List<List<string>> Codes { get; set; }

        /// <summary>Row-major ordered array of observation values.</summary>
        public List<double> Values { get; set; }
        public List<int> Statuses { get; set; }

        public List<string> GetCodes(int index) {
            List<string> codes = new List<string>(Dimensions.Count);

            for(int i = 0; i < Dimensions.Count; i++) {
                int pos = (int)(index / SizeWithin(i)) % Codes[i].Count;

                // Add the code for the index
                codes.Add(Codes[i][pos]);
            }

            return codes;
        }

        public int SizeWithin(int depth) {
            int size = 1;

            for(int i = Codes.Count-1; i > depth; i--) {
                size *= Codes[i].Count;
            }

            return size;
        }
    }
}
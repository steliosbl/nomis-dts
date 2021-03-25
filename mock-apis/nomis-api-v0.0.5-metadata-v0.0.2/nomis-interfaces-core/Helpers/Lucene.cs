using System.Collections.Generic;


namespace Nomis.Interfaces.Core.Helpers {
    public class Lucene {
        public static string BuildQuery(IDictionary<string, object> args, string joinWith = "AND") {
            // No arguments, so empty search string.
            if(args == null) return "";
            
            string fq = "";

            foreach(string key in args.Keys) {
                string value = args[key].ToString();

                if(fq.Length > 0) fq += $" {joinWith} ";
                fq += $"{key}:{value}";
            }

            return fq;
        }
    }
}
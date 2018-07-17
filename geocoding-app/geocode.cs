using System;
using System.Collections.Generic;
using System.Net;
using System.Threading.Tasks;
using System.Xml.Linq;
using Excel = Microsoft.Office.Interop.Excel;

namespace GISAPP
{
    class Pair
    {
        public Pair(string x, string y)
        {
            this.x = x;
            this.y = y;
        }

        public string x { get; set; }
        public string y { get; set; }
    }

    class Program
    {
        //dummy key, replace with google geocoding api key
        static string apikey = "244ef824193c024b3e3af50318ce7c66bdc8sdf";
        private static Object csvlock = new Object(); 

        static void Main(string[] args)
        {
            
            var d = readExcelSheet();


            int i = 0;

            Console.WriteLine(d.Count);

            try
            {
                using (System.IO.StreamWriter file =
                    new System.IO.StreamWriter(@"output.csv"))
                {
                    Pair p;
                    string data;
                    Parallel.ForEach(d, entry =>
                    {
                        data = entry.Value;

                        if (data.Contains("\""))
                        {
                            data = data.Replace("\"", "\"\"");
                        }

                        if (data.Contains(","))
                        {
                            data = String.Format("\"{0}\"", data);
                        }

                        if (data.Contains(System.Environment.NewLine))
                        {
                            data = String.Format("\"{0}\"", data);
                        }

                        p = GET(entry.Value);
                        lock (csvlock)
                        {
                            file.WriteLine(entry.Key + "," + data + "," + p.x + "," + p.y + ",");
                            Console.WriteLine("ENTRY: " + i);
                            i++;
                        }
                    });
                }
            }
            catch (Exception e)
            {
                Console.WriteLine(e);
                Console.Read();
            }

        }

        public static Pair GET(String address) {
            //string address = "4900 Meridian Street, Normal, AL 35762";
            string requestUri = string.Format("https://maps.googleapis.com/maps/api/geocode/xml?address={0}&key={1}", Uri.EscapeDataString(address),apikey);

            try
            {
                WebRequest request = WebRequest.Create(requestUri);
                WebResponse response = request.GetResponse();
                XDocument xdoc = XDocument.Load(response.GetResponseStream());

                XElement result = xdoc.Element("GeocodeResponse").Element("result");
                XElement locationElement = result.Element("geometry").Element("location");
                XElement lat = locationElement.Element("lat");
                XElement lng = locationElement.Element("lng");

                return new Pair(lat.Value, lng.Value);
            }
            catch (Exception e)
            {
                Console.WriteLine("EXCEPTION OCCURRED");
                Console.WriteLine(e);
                return new Pair("0","0");
            }
               
        }

        public static Dictionary<string, string> readExcelSheet()
        {

            //FORMAT DATA LIKE THIS: 
            //uniqueid, streetname, city, state, zip

            Dictionary<string, string> d = new Dictionary<string, string>(); 
            
            Excel.Application xlApp = new Excel.Application();
            Excel.Workbook xlWorkbook = (dynamic)xlApp.Workbooks.Open(@"inputfile.xlsx");
            Excel._Worksheet xlWorksheet = xlWorkbook.Sheets[1];
            Excel.Range xlRange = xlWorksheet.UsedRange;

            string name;
            string addy;

            for (int i = 1; i <= xlWorksheet.Rows.Count; i++)
            {
                if (i >= 11) break;
                Console.WriteLine(i);
                name = xlRange.Cells[i, 1].Value2.ToString();
                addy = xlRange.Cells[i, 2].Value2.ToString() + ", " + xlRange.Cells[i, 3].Value2.ToString() + ", " + xlRange.Cells[i, 4].Value2.ToString() + ", " + xlRange.Cells[i, 5].Value2.ToString();

                d[name] = addy;
                Console.WriteLine(name + "  :  "+addy);
            }

            return d;
        }

    }
}

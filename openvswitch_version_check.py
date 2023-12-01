import  requests


def get_cves_openvswitch(version):

    url = f"https://services.nvd.nist.gov/rest/json/cves/2.0?cpeName=cpe:2.3:a:openvswitch:openvswitch:{version}:*:*:*:*:*:*:*"
    #print(f"Constructed URL: {url}")
    response = requests.get(url)
    cve_list = []

    if response.status_code == 200:
        data = response.json()

        for results in data["vulnerabilities"]:
            cve_id = results["cve"]["id"]
            description = results["cve"]["descriptions"][0]["value"]    
            cvss_temp = results["cve"]["metrics"]

            if "cvssMetricV30" in cvss_temp:
                cvss = cvss_temp["cvssMetricV30"][0]["cvssData"]["baseScore"]
            elif "cvssMetricV31" in cvss_temp:
                cvss = cvss_temp["cvssMetricV31"][0]["cvssData"]["baseScore"]
            
            cve = {
                "id": cve_id,
                "description": description,
                "cvss": cvss
            }

            cve_list.append(cve)

        return cve_list
    
    else:
        print(f"Error: {response.status_code} - {response.reason}")
        return None
    
def average_cvss(cves):
    
        sum = 0
    
        for cve in cves:
            sum += cve["cvss"]
    
        return sum / len(cves)


def main():

    version_to_check = input("Enter Open vSwitch version (e.g., '2.5.0'): ")
    print()
    cves = get_cves_openvswitch(version_to_check)

    if cves:
        print(f"List of CVEs for Open vSwitch {version_to_check}:")
        print("........................................")
        print()

        for cve in cves:
            print(f"{cve['id']} (CVSS Base Score: {cve['cvss']}):")
            print(f"{cve['description']}")
            print()

        print(f"Total number of CVEs found: {len(cves)} ")
        print(f"Average CVSS Base Score: {average_cvss(cves)}")

    else:
        print("No CVEs found or there was an error.")

if __name__ == "__main__":
    main()
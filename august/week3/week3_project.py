import json

risks = ["Budget", "Timeline", "Technical"]


def analyze_risks(risks):
    risk_label={}
    for risk in risks:
        if risk=="Budget" or risk== "Timeline":
                risk_label[risk]= "High"
        else:
            risk_label[risk]= "Moderate"

    return(risk_label)
    

risk_label= analyze_risks(risks)
json_data = json.dumps(risk_label, indent=4)

with open("risk_report.json", "w") as file:
    file.write(json_data)

with open("risk_report.json", "r") as file:
    content = file.read()

risk_read=json.loads(content)

print(risk_read["Technical"])
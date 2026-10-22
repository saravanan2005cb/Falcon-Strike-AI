import json

def analyze_iam_security():
    print("[+] Starting Falcon Strike-AI Rapid Security Analysis...")
    
    try:
        # Load local mock data
        with open('mock_data.json', 'r') as f:
            data = json.load(f)
            
        users = data.get("Users", [])
        report = []
        
        for user in users:
            username = user.get("UserName")
            policies = user.get("AttachedPolicies", [])
            
            risk_level = "LOW"
            findings = []
            
            for policy in policies:
                if "AdministratorAccess" in policy.get("PolicyName", ""):
                    risk_level = "HIGH"
                    findings.append("User has full Administrator Access (Critical Security Risk).")
            
            user_report = {
                "UserName": username,
                "RiskLevel": risk_level,
                "Findings": findings
            }
            report.append(user_report)
            
        # Save analysis report
        with open('security_report.json', 'w') as rf:
            json.dump(report, rf, indent=2)
            
        print("[✓] Analysis Completed Successfully!")
        print("[✓] Report generated: 'security_report.json'")
        
        # Print summary
        print("\n--- Security Summary ---")
        for r in report:
            print(f"User: {r['UserName']} | Risk: {r['RiskLevel']}")
            for f in r['Findings']:
                print(f"  -> {f}")
                
    except Exception as e:
        print(f"[X] Error during analysis: {e}")

if __name__ == "__main__":
    analyze_iam_security()
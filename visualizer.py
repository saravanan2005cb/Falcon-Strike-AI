import json

def generate_html_report():
    print("[+] Generating Falcon Strike-AI Visual Dashboard...")
    
    try:
        with open('security_report.json', 'r') as f:
            reports = json.load(f)
            
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Falcon Strike-AI Security Report</title>
            <style>
                body { font-family: Arial, sans-serif; background-color: #1a1a2e; color: #fff; padding: 20px; }
                h1 { color: #e94560; text-align: center; }
                .card { background-color: #16213e; border-radius: 8px; padding: 20px; margin: 15px 0; border-left: 6px solid #e94560; }
                .user-name { font-size: 20px; font-weight: bold; color: #0f3460; background: #e94560; display: inline-block; padding: 4px 12px; border-radius: 4px; color: white; }
                .risk-high { color: #ff4d4d; font-weight: bold; }
                .finding { background: #0f3460; padding: 10px; border-radius: 4px; margin-top: 10px; }
            </style>
        </head>
        <body>
            <h1>🦅 Falcon Strike-AI: IAM Security Dashboard</h1>
            <p style="text-align:center;">Automated Graph Analysis & Attack Path Identification</p>
            <hr>
        """
        
        for r in reports:
            html_content += f"""
            <div class="card">
                <span class="user-name">User: {r['UserName']}</span>
                <p><strong>Risk Assessment:</strong> <span class="risk-high">{r['RiskLevel']}</span></p>
                <div class="finding">
                    <strong>Critical Findings / Attack Vectors:</strong>
                    <ul>
            """
            for finding in r['Findings']:
                html_content += f"<li>{finding}</li>"
                
            html_content += """
                    </ul>
                </div>
            </div>
            """
            
        html_content += """
        </body>
        </html>
        """
        
        with open('index.html', 'w') as hf:
            hf.write(html_content)
            
        print("[✓] Visual Dashboard generated successfully: 'index.html'")
        print("[*] Open 'index.html' in your browser to view the report!")
        
    except Exception as e:
        print(f"[X] Error generating visual report: {e}")

if __name__ == "__main__":
    generate_html_report()
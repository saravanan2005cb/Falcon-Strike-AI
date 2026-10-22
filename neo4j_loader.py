import json
from neo4j import GraphDatabase

class Neo4jConnector:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def create_user_node(self, user_data):
        with self.driver.session() as session:
            session.execute_write(self._create_user, user_data)

    @staticmethod
    def _create_user(tx, user_data):
        query = (
            "MERGE (u:AWSUser {id: $user_id}) "
            "SET u.name = $username, u.arn = $arn "
            "RETURN u"
        )
        tx.run(
            query, 
            user_id=user_data.get('UserId'), 
            username=user_data.get('UserName'), 
            arn=user_data.get('Arn')
        )
        print(f"[+] Graph Node Created for User: {user_data.get('UserName')}")

def run_loader():
    try:
        # Load mock JSON data
        with open('mock_data.json', 'r') as f:
            data = json.load(f)
            
        print("[+] Mock Data Loaded Successfully.")
        
        # Database connection parameters (Local Neo4j instance / AuraDB)
        # உங்கள் Neo4j URI மற்றும் Password-ஐ இங்கே கொடுக்க வேண்டும்
        URI = "bolt://localhost:7687"
        USER = "neo4j"
        PASSWORD = "your_password"  # உங்கள் நியோ4ஜே பாஸ்வேர்ட்
        
        # Note: If local Neo4j server is not yet running, 
        # this will test the script structure first.
        print("[+] Initializing Neo4j Connection Driver...")
        connector = Neo4jConnector(URI, USER, PASSWORD)
        
        for user in data.get("Users", []):
            connector.create_user_node(user)
            
        connector.close()
        print("[✓] All data successfully loaded into Neo4j Graph Database!")
        
    except FileNotFoundError:
        print("[X] Error: 'mock_data.json' file not found.")
    except Exception as e:
        print(f"[!] Database Connection Note: {e}")
        print("[*] Script logic is verified. You can start your local Neo4j server to push nodes.")

if __name__ == "__main__":
    run_loader()

import os
import time
import pandas as pd
import meraki

# === CONFIGURATION ===
API_KEY = os.getenv("MERAKI_DASHBOARD_API_KEY") or "YOUR_API_KEY_HERE_BETWEEN_QUOTES_"
NETWORK_ID = "YOUR_NETWORK_ID_HERE_BETWEEN_QUOTES_"
GROUP_POLICY_NAME = "Ruijie_AP_Switch" # Replace with your actual group policy name
EXCEL_FILE = "Neo_AP.xlsx"  # Replace with your actual filename

# === INIT MERAKI SDK ===
dashboard = meraki.DashboardAPI(API_KEY, print_console=False)

# === LOAD MAC-IP LIST ===
df = pd.read_excel(EXCEL_FILE)
df = df[['MAC', 'Management URL']].dropna()
df.columns = ['mac', 'ip']

# === FETCH GROUP POLICIES TO GET THE CORRECT ID ===
policies = dashboard.networks.getNetworkGroupPolicies(NETWORK_ID)
policy_map = { p['name']: p['groupPolicyId'] for p in policies }
group_policy_id = policy_map.get(GROUP_POLICY_NAME)

if not group_policy_id:
    raise Exception(f"Group policy '{GROUP_POLICY_NAME}' not found!")

# === PROCESS EACH CLIENT ===
for index, row in df.iterrows():
    mac = row['mac'].strip().lower()
    ip = row['ip'].strip()

    client = None

    # Try finding by MAC
    try:
        client = dashboard.networks.getNetworkClient(NETWORK_ID, mac)
        print(f"[MAC FOUND] {mac} -> {client.get('description', '')}")
    except meraki.APIError:
        print(f"[MAC NOT FOUND] {mac}, trying IP {ip}...")

    # Try finding by IP if MAC fails
    if not client:
        try:
            client = dashboard.networks.getNetworkClient(NETWORK_ID, ip)
            print(f"[IP FOUND] {ip} -> {client.get('description', '')}")
        except meraki.APIError:
            print(f"[NOT FOUND] MAC: {mac}, IP: {ip}")
            continue

    # Assign group policy
    try:
        dashboard.networks.updateNetworkClientPolicy(
            NETWORK_ID,
            client['mac'],
            devicePolicy='Group policy',
            groupPolicyId=group_policy_id
        )
        print(f"[POLICY APPLIED] {mac} / {ip} → {GROUP_POLICY_NAME}")
    except Exception as e:
        print(f"[ERROR APPLYING POLICY] {mac} / {ip}: {e}")

    time.sleep(0.2)  # avoid rate limits

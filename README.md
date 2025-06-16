
# Meraki Group Policy Automation Tool

This repository helps you bulk-assign a **Meraki Group Policy** (e.g., `Ruijie_AP_Switch`) to devices by matching either their **MAC address** or **IP address**. It’s especially helpful in large networks where you have a list of devices exported to Excel but not all are immediately visible in the Meraki dashboard via MAC lookup.

---

## 🧠 Why This Exists (Real-World Use Case)

As the IT person of few sites, I manage over 130+ **Ruijie Access Points** spread across rooms, function halls, and lobbies — all connected to **Meraki switches**.

Ruijie’s AP dashboard handles **speed limits and AP behavior**, but the uplinks pass through Meraki. Without assigning the right **Group Policy** on Meraki, traffic shaping or firewall exceptions (like DNS or POS systems) may not work correctly.

Manually assigning Group Policies to each MAC in Meraki's UI is painfully slow or maybe I'm lazy person 😁.

> That’s why I built this tool: to bulk-assign policies using MAC or IP address, directly from a spreadsheet dump exported from the Ruijie cloud portal or local switch scans.

Whether you're deploying 5 or 500 APs — this saves hours and minimizes human error.

---

## 🔧 What It Does

- Reads a list of MAC and IP addresses from an Excel file
- Uses the Meraki Dashboard API to:
  - Fetch available group policies in a given network
  - Search for clients using MAC address first, then fallback to IP address
  - Apply the desired group policy to matched devices

---

## 📁 File Structure

```
.
├── apply_group_policy_mac_ip_fallback.py   # Main Python script
├── Neo_AP.xlsx                             # Excel sheet with MAC/IP list
├── README.md                               # You're reading it 😉
```

---

## 📋 Prerequisites

- Python 3.9+
- Installed modules:
  ```bash
  pip install meraki 
  ```
- Meraki API key with write access to your organization

---

## 🧪 Sample Excel Format (`Neo_AP.xlsx`)

| MAC of your device or AP                | Management URL (Basically DHCP IP from Meraki) |
|--------------------|----------------|
| c8:cd:55:95:e1:5c  | 10.3.13.17     |
| d4:31:27:7b:d5:10  | 10.3.13.73     |
| ...                | ...            |

> Only two columns: **MAC** and **Management URL**. No headers renaming required.

---

## 🚀 How to Use

1. **Edit Configurations in Python Script**

   ```python
   API_KEY = os.getenv("MERAKI_DASHBOARD_API_KEY") or "<your_api_key>"
   NETWORK_ID = "<your_network_id>"
   GROUP_POLICY_NAME = "Ruijie_AP_Switch"  # or any policy name you want to apply
   EXCEL_FILE = "Neo_AP.xlsx"
   ```

2. **Run the Script**
   ```bash
   python apply_group_policy_mac_ip_fallback.py
   ```

3. **Watch the Output**
   The script logs:
   - Whether MAC or IP was found
   - If group policy was successfully applied

---

## 🖼️ Some Screenshots
![a04ffe69-1b08-4533-943c-e3d2ff6b65b4](https://github.com/user-attachments/assets/b6b2b8c1-0b9d-47d8-8866-f2ddc1fa3f63)
![image](https://github.com/user-attachments/assets/f6e61bbd-c429-49b8-83cf-5e4421d41f4d)



---

## 📌 Notes

- Group policy name must **exactly** match what’s defined in the Meraki dashboard.
- This script is non-destructive. It only assigns policies — no deletion or modification of other attributes.
- Add a `time.sleep(0.2)` to avoid hitting API rate limits (done by default).

---

## 🙋‍♂️ Maintainer

**Deadboy**  
📧 Drop issues or pull requests if you'd like to improve the tool.

---

## 📜 License

MIT. Free to use, tweak, and share.

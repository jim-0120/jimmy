from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

# 設定 Chrome 瀏覽器選項
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # 啟用無頭模式，不顯示瀏覽器畫面
options.add_argument("--disable-gpu")  # 禁用 GPU 加速
options.add_argument("--no-sandbox")  # 禁用沙盒模式
options.add_argument("--disable-blink-features=AutomationControlled")  # 防止被網站偵測為自動化工具
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36")  # 模擬真實瀏覽器的 User-Agent

# 初始化 Chrome 瀏覽器
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
url = "https://www.spotrac.com/mlb/free-agents/_/year/2025"  # 目標頁面 URL
driver.get(url)  # 開啟目標頁面
time.sleep(5)  # 等待頁面載入完成，確保 JavaScript 加載表格資料

# 資料儲存清單，將來用來存儲每一行的球員資料
data_list = []

# 定位並抓取表格中所有資料列
rows = driver.find_elements(By.CSS_SELECTOR, 'tbody tr')  # 使用 CSS Selector 找到所有 <tr> 標籤，這些是表格資料列

# 遍歷每一列資料
for row in rows:
    cols = row.find_elements(By.TAG_NAME, 'td')  # 每一列的 <td> 標籤代表一個資料欄位
    if len(cols) >= 7:  # 確保這一列有足夠的資料欄位（通常是 7 個）
        # 提取各欄位的資料並組成字典
        data = {
            "Player": cols[0].text.strip(),  # 球員名稱
            "Position": cols[1].text.strip(),  # 球員位置
            "Age": cols[2].text.strip(),  # 球員年齡
            "Team": cols[3].text.strip(),  # 球隊名稱
            "2025 AAV": cols[4].text.strip(),  # 2025 年的年均薪資（AAV）
            "Free Agent Type": cols[5].text.strip(),  # 自由球員類型（例如：一般自由球員）
            "2024 Salary": cols[6].text.strip(),  # 2024 年薪資（根據需要）
        }
        # 將抓取到的資料加入到資料列表
        data_list.append(data)
        print(data)  # 印出每一行資料，方便檢查

# 關閉瀏覽器，避免資源浪費
driver.quit()

# 使用 pandas 將抓取到的資料轉換成 DataFrame 並儲存為 CSV 檔案
df = pd.DataFrame(data_list)  # 將資料列表轉換為 DataFrame
df.to_csv("spotrac_mlb_free_agents_2025.csv", index=False, encoding="utf-8-sig")  # 儲存為 CSV，避免編碼問題
print("資料已儲存：spotrac_mlb_free_agents_2025.csv")  # 輸出提示訊息，確認儲存完成

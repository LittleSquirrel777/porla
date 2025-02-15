from flask import Flask, request, jsonify
from flask_cors import cross_origin, CORS
import json
import subprocess
import random
import concurrent.futures
import hashlib

'''
     使用request接收前端post请求
     直接使用return发送后端处理好的数据给前端
'''
#	flask服务启动，进行初始化
app = Flask(__name__)
CORS(app)
# databseName = "/..."
serverPath = "/home/lishuai/porla/porla/porla/Server/Server"
clientPath = "/home/lishuai/porla/porla/porla/Client/Client"
serverOutputFile = "/data/ls/data_config_file/log/data_server_output"
clientOutputFile = "/data/ls/data_config_file/log/data_client_output"

databaseName_to_config_and_blockCount = {
    "email_txt": {"config_path": "/data/ls/data_config_file/email_txt", "blockCount": 2097152, "highest_level_index": 21, "destroy_blocks": [], "pre_hash": [], "destroy_hash": []},
    "img_m": {"config_path": "/data/ls/data_config_file/img_m", "blockCount": 4194304, "highest_level_index": 22, "destroy_blocks": [], "pre_hash": [], "destroy_hash": []},
    "img_million": {"config_path": "/data/ls/data_config_file/img_m", "blockCount": 4194304, "highest_level_index": 22, "destroy_blocks": [], "pre_hash": [], "destroy_hash": []},
    "text": {"config_path": "/data/ls/data_config_file/img_txt/text", "blockCount": 8192, "highest_level_index": 13, "destroy_blocks": [], "pre_hash": [], "destroy_hash": []},
}

# destroy_block_path = "/home/kt3/porla/porla/porla/Server/destroy_block"
destroy_log_path = "/data/ls/data_config_file/log/destroy_log.txt"
@app.route('/audit', methods=['POST', 'GET'])
@cross_origin(origins=["http://10.201.153.203:8001"], methods=["GET", "POST"], allow_headers=["Content-Type"], withCredentials=True)
def audit():
    if request.method == 'POST':
        data = request.get_json(silent=True)
        print(data)
        result = audit_process(data)
        with open(destroy_log_path, "+a", encoding="utf-8") as file:
            file.writelines(f"{data['databaseName']} audit\n")
        return jsonify(result)
    else:
        return " 'it's not a POST operation! "


@app.route('/destroy_location', methods=['POST', 'GET'])
@cross_origin(origins=["http://10.201.153.203:8001"], methods=["GET", "POST"], allow_headers=["Content-Type"], withCredentials=True)
def destroy_location():
    if request.method == 'POST':
        data = request.get_json(silent=True)
        retData = {
            "location": databaseName_to_config_and_blockCount[data["databaseName"]]["destroy_blocks"],
            "pre_hash": databaseName_to_config_and_blockCount[data["databaseName"]]["pre_hash"],
            "des_hash": databaseName_to_config_and_blockCount[data["databaseName"]]["destroy_hash"],
        }
        with open(destroy_log_path, "+a", encoding="utf-8") as file:
            file.writelines(f"{data['databaseName']} location\n")
        return jsonify(retData)
    else:
        return " 'it's not a POST operation! "

@app.route('/destroy', methods=['POST', 'GET'])
@cross_origin(origins=["http://10.201.153.203:8001"], methods=["GET", "POST"], allow_headers=["Content-Type"], withCredentials=True)
def destroy():
    if request.method == 'POST':
        data = request.get_json(silent=True)
        destroy_process(data)
        retData = {
            "location": databaseName_to_config_and_blockCount[data["databaseName"]]["destroy_blocks"],
            "pre_hash": databaseName_to_config_and_blockCount[data["databaseName"]]["pre_hash"],
            "des_hash": databaseName_to_config_and_blockCount[data["databaseName"]]["destroy_hash"],
        }
        with open(destroy_log_path, "+a", encoding="utf-8") as file:
            file.writelines(f"{data['databaseName']} destroy\n")
            json.dump(retData, file, ensure_ascii=False)
            file.writelines("\n")
        return jsonify(retData)
    

@app.route('/recovery', methods=['POST', 'GET'])
@cross_origin(origins=["http://10.201.153.203:8001"], methods=["GET", "POST"], allow_headers=["Content-Type"], withCredentials=True)
def recovery():
    if request.method == 'POST':
        data = request.get_json(silent=True)
        retData = {}
        if len(databaseName_to_config_and_blockCount[data["databaseName"]]["destroy_blocks"]) == 0:
            retData["state"] = "failed"
        else:
            recovery_process(data)
            retData["state"] = "success"
        with open(destroy_log_path, "+a", encoding="utf-8") as file:
            file.writelines(f"{data['databaseName']} recovery\n")
            json.dump(retData, file, ensure_ascii=False)
            file.writelines("\n")
        return jsonify(retData)

def audit_process(data):
    databaseName = data["databaseName"]
    
    try:
        serverProcess = None
        serverProcess = subprocess.Popen([serverPath, databaseName], shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        clientProcess = subprocess.Popen([clientPath, databaseName], shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        returncode = clientProcess.wait()
        # print(f"returncode:{returncode}\n")
        if returncode != 0:
            raise subprocess.CalledProcessError(returncode, clientProcess)
    except Exception as e:
        return {"blockCount": databaseName_to_config_and_blockCount[data["databaseName"]]["blockCount"], "auditResult": "Failed", "totalAuditTime": "-",
            "readTime": "-", "computeTime": "-", "preparationTime": "-", "proveTime": "-"
        }
    finally:
        if serverProcess is not None:
            serverProcess.kill()
            serverProcess.wait()

    with open(clientOutputFile) as file:
        line = file.readline()
        _, totalAuditTime = line.strip().split(":")
        totalAuditTime = float(totalAuditTime) / 1000
    with open(serverOutputFile) as file:
        line = file.readline()
        _, readTime = line.strip().split(":")
        readTime = float(readTime) / 1000
        line = file.readline()
        _, computeTime = line.strip().split(":")
        computeTime = float(computeTime) / 1000
        line = file.readline()
        _, preparationTime = line.strip().split(":")
        preparationTime = float(preparationTime) / 1000
        line = file.readline()
        _, proveTime = line.strip().split(":")
        proveTime = float(proveTime) / 1000
    data = {"blockCount": databaseName_to_config_and_blockCount[data["databaseName"]]["blockCount"], "auditResult": "Success", "totalAuditTime": str(totalAuditTime) + "ms", 
        "readTime": str(readTime) + "ms", "computeTime": str(computeTime) + "ms", "preparationTime": str(preparationTime) + "ms", "proveTime": str(proveTime) + "ms"
    }
    
    return data

def destroy_process(data):
    destroyBlocks = databaseName_to_config_and_blockCount[data["databaseName"]]["destroy_blocks"]
    pre_hash = databaseName_to_config_and_blockCount[data["databaseName"]]["pre_hash"]
    destroy_hash = databaseName_to_config_and_blockCount[data["databaseName"]]["destroy_hash"]
    flag = False
    if len(destroyBlocks) != 0:
        with open(destroy_log_path, "+a", encoding="utf-8") as file:
            file.writelines("last database not recovery!!!\n")
        flag = True
    config_path = databaseName_to_config_and_blockCount[data["databaseName"]]["config_path"]
    blockCount = databaseName_to_config_and_blockCount[data["databaseName"]]["blockCount"]
    level = databaseName_to_config_and_blockCount[data["databaseName"]]["highest_level_index"]
    num_workers = 20
    # with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
    #     futures = []
    #     for i in range(int(blockCount / 100)):
    #         destroyNum = random.randint(0, blockCount - 1)
    #         if not flag:
    #             while destroyNum in destroyBlocks:
    #                 destroyNum = random.randint(0, blockCount - 1)
    #         if destroyNum not in destroyBlocks:
    #             # destroyBlocks.append(destroyNum)
    #             futures.append(executor.submit(destroy_subprocess, destroyNum, config_path, level, destroyBlocks, pre_hash, destroy_hash))
    #             # write_number_to_first_line(f"{config_path}/H_X/{level}_{destroyNum}")
    #             # write_number_to_first_line(f"{config_path}/H_Y/{level}_{destroyNum}")

    #         if len(futures) >= num_workers:
    #             for future in concurrent.futures.as_completed(futures):
    #                 future.result()
    #             futures = []
    #     for future in concurrent.futures.as_completed(futures):
    #         future.result()
    for i in range(int(blockCount / 100)):
        destroyNum = random.randint(0, blockCount - 1)
        if not flag:
            while destroyNum in destroyBlocks:
                destroyNum = random.randint(0, blockCount - 1)
        if destroyNum not in destroyBlocks:
            destroy_subprocess(destroyNum, config_path, level, destroyBlocks, pre_hash, destroy_hash)
    print(len(destroyBlocks))
    print(len(pre_hash))
    print(len(destroy_hash))

def destroy_subprocess(destroyNum, config_path, level, destroyBlocks, pre_hash, destroy_hash):
    destroyBlocks.append(destroyNum)
    hash_value = calculate_file_hash(f"{config_path}/H_X/{level}_{destroyNum}")
    pre_hash.append(hash_value)
    write_number_to_first_line(f"{config_path}/H_X/{level}_{destroyNum}")
    write_number_to_first_line(f"{config_path}/H_Y/{level}_{destroyNum}")
    destroy_hash_value = calculate_file_hash(f"{config_path}/H_X/{level}_{destroyNum}")
    destroy_hash.append(destroy_hash_value)

def recovery_process(data):
    config_path = databaseName_to_config_and_blockCount[data["databaseName"]]["config_path"]
    level = databaseName_to_config_and_blockCount[data["databaseName"]]["highest_level_index"]
    destroyBlocks = databaseName_to_config_and_blockCount[data["databaseName"]]["destroy_blocks"]
    # num_workers = 20
    # with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
    #     futures = []
    #     for destroyNum in destroyBlocks:
    #         futures.append(executor.submit(recovery_subprocess, destroyNum, config_path, level))
    #         if len(futures) >= num_workers:
    #             for future in concurrent.futures.as_completed(futures):
    #                 future.result()
    #             futures = []
    #     for future in concurrent.futures.as_completed(futures):
    #         future.result()
    for destroyNum in destroyBlocks:
        recovery_subprocess(destroyNum, config_path, level)
    databaseName_to_config_and_blockCount[data["databaseName"]]["destroy_blocks"] = []
    databaseName_to_config_and_blockCount[data["databaseName"]]["pre_hash"] = []
    databaseName_to_config_and_blockCount[data["databaseName"]]["destroy_hash"] = []

def recovery_subprocess(destroyNum, config_path, level):
    remove_first_line(f"{config_path}/H_X/{level}_{destroyNum}")
    remove_first_line(f"{config_path}/H_Y/{level}_{destroyNum}")

def write_number_to_first_line(file_path):
    with open(file_path, 'rb') as file:
        lines = file.readlines()
    lines.insert(0, b'123\n')
    with open(file_path, 'wb') as file:
        file.writelines(lines)

def remove_first_line(file_path):
    with open(file_path, 'rb') as file:
        lines = file.readlines()
    if lines:
        lines = lines[1:]
    with open(file_path, 'wb') as file:
        file.writelines(lines)

def calculate_file_hash(file_path, hash_algorithm='sha256'):
    # 创建哈希对象
    hash_obj = hashlib.new(hash_algorithm)
    # 以二进制方式读取文件，并逐块更新哈希值
    with open(file_path, 'rb') as file:
        while chunk := file.read(8192):
            hash_obj.update(chunk)
    # 返回哈希值的十六进制表示
    return hash_obj.hexdigest()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=7002)
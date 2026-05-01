# Teste_ROS2
## 🤖 Controle de Robô UR10 com ROS 2

Este repositório descreve o processo de configuração, conexão e execução de movimentos em um robô UR10 a partir do driver da UR em ROS2, utilizando o ur_robot_driver e um script personalizado em Python feita pela equipe do Iris Lab para enviar trajetórias ao robô.

## 🔌 1. Conexão com o robô
### Conecte o cabo Ethernet do robô ao notebook
Configure a rede cabeada (IPv4):

```bash
IP: 192.168.0.XX
Máscara: 255.255.255.0
Gateway: 0.0.0.0
```
Verifique seu IP:
```bash
ip a
```
ou
```bash
hostname -I
```
Ative o External Control no robô, coloque o ip do computador e teste a conexão:
```bash
ping 192.168.0.10
```
Verifique a porta de comunicação:
```bash
nc -zv 192.168.0.10 50002
```

Se houver conflito na porta:
```bash
sudo fuser -k 50002/tcp
sudo lsof -i :50002
```
Desative o firewall:
```bash
sudo ufw disable
```
## ⚙️ 2. Configuração inicial do workspace
```bash
cd ~/workspaces/ur_gazebo
source install/setup.bash
```
## 📐 3. Calibração do robô

Execute apenas uma vez:
```bash
ros2 launch ur_calibration calibration_correction.launch.py \
robot_ip:=192.168.0.10 \
target_filename:="${HOME}/my_robot_calibration.yaml"
```
Esse comando extrai os parâmetros reais do robô e melhora a precisão dos movimentos.

## 🚀 4. Executando o driver do robô
```bash
ros2 launch ur_robot_driver ur_control.launch.py \
ur_type:=ur10 \
robot_ip:=192.168.0.10 \
kinematics_params_file:="${HOME}/my_robot_calibration.yaml" \
initial_joint_controller:=joint_trajectory_controller
```
## 📌 Observações:

 No teach pendant:
 * Coloque o robô em HOME
 * Clique em PLAY

## 🦾 5. Teste com controlador padrão

Em outro terminal:
```bash
cd ~/workspaces/ur_gazebo
source install/setup.bash
ros2 launch ur_robot_driver test_joint_trajectory_controller.launch.py
```
O robô deve iniciar movimento em até ~10 segundos.

Após o teste inicial com o código acima da própria UR, a equipe do IrisLab desenvolveu seu próprio código em Python.
## 🐍 6. Script personalizado (envia_trajetoria)
Criando o pacote:
```bash
cd ~/workspaces/ur_gazebo/src
ros2 pkg create --build-type ament_python meu_projeto_ur --dependencies rclpy trajectory_msgs
```

### Estrutura do projeto criada:
Insira o código em Python dentro da árvore do programa criada. Aqui no exemplo inserimos o script.py.
```
meu_projeto_ur/
 └── meu_projeto_ur/
     └── script.py
```
Permissão de execução:
```bash
chmod +x script.py
```
Configurando o setup.py
```
entry_points={
    'console_scripts': [
        'envia_trajetoria = meu_projeto_ur.script:main',
    ],
},
```
Compilando:
```bash
cd ~/workspaces/ur_gazebo
colcon build --packages-select meu_projeto_ur
source install/setup.bash
```
### Executando o script:
*Um terminal deve estar rodando o driver do robô e estar apertado o play no teach pendant.
* No outro terminal rodamos o script.
```bash
ros2 run meu_projeto_ur envia_trajetoria
```

## Vídeo do robô movendo via ROS2
[![Ver vídeo](https://img.youtube.com/vi/1SLCnnARI1k/0.jpg)](https://youtube.com/shorts/1SLCnnARI1k)

# Teste_ROS2
🤖 Controle de Robô UR10 com ROS 2

Este repositório descreve o processo de configuração, conexão e execução de movimentos em um robô UR10 utilizando o ur_robot_driver e um script personalizado em Python feita pela equipe do Iris Lab.

🔌 1. Conexão com o robô
Conecte o cabo Ethernet do robô ao notebook
Configure a rede cabeada (IPv4):
'''bash
IP: 192.168.0.XX
Máscara: 255.255.255.0
Gateway: 0.0.0.0
'''
Verifique seu IP:
'''bash
ip a
'''
ou
'''bash
hostname -I
'''
Teste a conexão com o robô:
'''bash
ping 192.168.0.10
'''
Verifique a porta de comunicação:
'''bash
nc -zv 192.168.0.10 50002
'''

Se houver conflito na porta:
'''bash
sudo fuser -k 50002/tcp
sudo lsof -i :50002
'''
Desative o firewall:
sudo ufw disable
⚙️ 2. Configuração inicial do workspace
cd ~/workspaces/ur_gazebo
source install/setup.bash
📐 3. Calibração do robô

Execute apenas uma vez:

ros2 launch ur_calibration calibration_correction.launch.py \
robot_ip:=192.168.0.10 \
target_filename:="${HOME}/my_robot_calibration.yaml"

Esse comando extrai os parâmetros reais do robô e melhora a precisão dos movimentos.

🚀 4. Executando o driver do robô
ros2 launch ur_robot_driver ur_control.launch.py \
ur_type:=ur10 \
robot_ip:=192.168.0.10 \
kinematics_params_file:="${HOME}/my_robot_calibration.yaml" \
initial_joint_controller:=joint_trajectory_controller

📌 Observações:

Abra o RViz para visualizar o robô
No teach pendant:
Coloque o robô em HOME
Ative o programa External Control
Clique em PLAY

Se necessário, limpe processos:

pkill -f ros2
pkill -f ur_control
🦾 5. Teste com controlador padrão

Em outro terminal:

cd ~/workspaces/ur_gazebo
source install/setup.bash

ros2 launch ur_robot_driver test_joint_trajectory_controller.launch.py

O robô deve iniciar movimento em até ~10 segundos.

🐍 6. Script personalizado (envia_trajetoria)
Criando o pacote:
cd ~/workspaces/ur_gazebo/src

ros2 pkg create --build-type ament_python meu_projeto_ur \
--dependencies rclpy trajectory_msgs
Estrutura:
meu_projeto_ur/
 └── meu_projeto_ur/
     └── my_robot.py
Permissão de execução:
chmod +x my_robot.py
Configurando o setup.py
entry_points={
    'console_scripts': [
        'envia_trajetoria = meu_projeto_ur.my_robot:main',
    ],
},
Compilando:
cd ~/workspaces/ur_gazebo
colcon build --packages-select meu_projeto_ur
source install/setup.bash
Executando o script:

⚠️ Antes:

Driver do robô rodando
Teach pendant em PLAY
ros2 run meu_projeto_ur envia_trajetoria
🔁 7. Fluxo completo de execução
Configurar rede
Rodar driver (ur_control.launch.py)
Dar PLAY no robô
Rodar:
Teste padrão (test_joint_trajectory_controller) ou
Script próprio (envia_trajetoria)

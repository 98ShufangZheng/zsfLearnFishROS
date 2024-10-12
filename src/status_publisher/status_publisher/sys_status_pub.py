import rclpy
from status_interfaces.msg import SystemStatus
from rclpy.node import Node
import psutil
import platform

class SysStatusPub(Node):
    def __init__(self,node_name):
        super().__init__(node_name)
        self.status_publisher_ = self.create_publisher(SystemStatus, 'sys_status', 10)
        self.timer_ = self.create_timer(1.0,self.timer_callback)

    def timer_callback(self):
        cpu_percent = psutil.cpu_percent()  # 获取cpu百分比
        memory_info = psutil.virtual_memory()  # 获取内存信息
        net_io_counters = psutil.net_io_counters()  # 获取网络相关的输入输出信息

        # 组装一下消息
        msg = SystemStatus()
        msg.stamp = self.get_clock().now().to_msg()
        msg.host_name = platform.node()
        msg.cpu_percent = cpu_percent
        msg.memory_percent = memory_info.percent
        msg.memory_total = memory_info.total /1024 /1024
        msg.memory_available = memory_info.available /1024 /1024
        msg.net_sent = net_io_counters.bytes_sent /1024 /1024
        msg.net_recv = net_io_counters.bytes_recv /1024 /1024

        self.get_logger().info*(f'发布：{str(msg)}')
        self.status_publisher_.publish(msg)

def main():
    rclpy.init()
    node = SysStatusPub('sys_status_pub')
    rclpy.spin(node)
    rclpy.shutdown()
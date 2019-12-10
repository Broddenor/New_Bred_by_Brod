using System;
//using System.Collections.Generic;
//using System.Linq;
using System.Text;
using System.Threading;
using System.Windows;
/*using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;*/
using System.Diagnostics;
using Microsoft.Win32;
using System.Reflection;
// including the M2Mqtt Library
using uPLibrary.Networking.M2Mqtt;
using uPLibrary.Networking.M2Mqtt.Messages;


namespace WpfApp1
{
    public partial class MainWindow : Window
    {
        Process[] proc;
        MqttClient client;
        string clientId;
        string Password;
        bool pass_second_message = false;
        bool closing = false;

        [System.Runtime.InteropServices.DllImport("user32.dll", CharSet = System.Runtime.InteropServices.CharSet.Auto)]
        private static extern IntPtr GetKeyboardLayout(int WindowsThreadProcessID); //Импорт библиотеки для инцилизации расскладки клавиатуры

        System.Windows.Threading.DispatcherTimer timer = new System.Windows.Threading.DispatcherTimer(); //Ввод таймера

        public MainWindow()
        {
            InitializeComponent();
            //string BrokerAddress = "broker.hivemq.com";    //адрес глобального сервера 
            string BrokerAddress = "192.168.11.1";          //адрес локального сервера
            client = new MqttClient(BrokerAddress);        //инцилизация клиента для подключения

            // инцилизация функции для получения сообщений
            client.MqttMsgPublishReceived += client_MqttMsgPublishReceived;

            // инцилизация Id клиента
            clientId = Guid.NewGuid().ToString();
            try         // попытка подключения
            {
                client.Connect(clientId);       // подключение к топикам
            }
            catch       // если не удалось, ввывод Message Box и закрытие приложения
            {
                MessageBox.Show("Отсутсвует подключение к серверу, подключитесь к серверу и повторите попытку", "Error", MessageBoxButton.OK, MessageBoxImage.Error);
                closing = true;
                Close();
            }
            timer.Tick += new EventHandler(timerTick);          // объявление ивента для таймера 
            timer.Interval = new TimeSpan(0, 0, 1/10);         // установка времени таймера 
            timer.Start();                                    // запуск таймера
            //SetAutoload(true);
        }

        // ивент для закрытия программы

        public void OnClosed(object sender, System.ComponentModel.CancelEventArgs e)
        {
            if (closing != true)        // проверка переменной для закрытия программы
            {
                e.Cancel = true;        // не даёт закрыть программу, пока условие выполненяется
            }
            else
            {
                try
                {
                    Process proces = new Process();
                    proces.StartInfo.FileName = "C:\\Windows\\explorer.exe";
                    proces.StartInfo.UseShellExecute = true;
                    proces.Start();
                }
                catch { };
                try
                {
                    client.Disconnect(); // Попытка отключения от топиков
                }
                catch { }
                base.OnClosed(e);       // удаление переменных, функций из RAM
                Thread.Sleep(2000);
                App.Current.Shutdown(); // корректное заркытие программы
            }
        }

        // код для проверки правильности ввода пароля

        private void Pub_Click(object sender, RoutedEventArgs e)
        {
            if (Pass_Box.Password == txtReceived.Text)  // проверка содержимиого Pass Box, на последнее сообщение
            {
                closing = true;                                                  // доступ для закрытия приложения
                client.Publish("Pass_check", Encoding.UTF8.GetBytes("True"));   // публикация топика о корректно введённом пароле
                timer.Start();                                                 // запуск первого таймера
            }
            else // сообщение о неверном пароле
            {
                MessageBox.Show("Неверный пароль, введите верный пароль (возможно у вас включён CapsLock или выключен NumPad)", "Error", MessageBoxButton.OK, MessageBoxImage.Error);
            }
        }

        // ивент для приходящего сообщения

        void client_MqttMsgPublishReceived(object sender, MqttMsgPublishEventArgs e)
        {
            string ReceivedMessage = Encoding.UTF8.GetString(e.Message);            // перевод сообщения в текстовый формат
            Dispatcher.Invoke(delegate { txtReceived.Text = ReceivedMessage; });    // запись сообщения в Text.received
        }

        // таймер, первый

        private void timerTick(object sender, EventArgs e)
        {
            client.Subscribe(new string[] { "Users_name" }, new byte[] { 2 });  // подключение к топику
            this.Close();   // попытка зарыть приложение

            try
            {
                proc = Process.GetProcessesByName("cmd");
                proc[0].Kill();
            }
            catch { }
            try
            {
                proc = Process.GetProcessesByName("Taskmgr");
                proc[0].Kill();
            }
            catch { }
            try
            {
                proc = Process.GetProcessesByName("explorer");
                proc[0].Kill();
            }
            catch { }
            if ((txtReceived.Text != "false") && (pass_second_message == false))    // проверка о корректом распознании
            {
                timer.Stop();       // остановка таймера
                MessageBoxResult result = MessageBox.Show("Вы " + txtReceived.Text + "? Если Да, нажмите Да и введите пароль Если возникла ошибка, нажмите Нет и повторите распознование.", "Приветсвие", MessageBoxButton.YesNo, MessageBoxImage.Question);
                if (result == MessageBoxResult.Yes)     // если пользователь потвердил, что это он
                {

                    System.Windows.Threading.DispatcherTimer timer3 = new System.Windows.Threading.DispatcherTimer(); // инцилизация таймера для раскладки клавиатуры

                    timer3.Tick += new EventHandler(timerTick3);        // ввод ивента
                    timer3.Interval = new TimeSpan(0, 0, 1 / 10);       // ввод времени 
                    timer3.Start();                                     // запуск таймера


                    client.Publish("Message_check", Encoding.UTF8.GetBytes("1"));   // публикация сообщения о корректном пользователе

                    client.Subscribe(new string[] { "Pass_throw" }, new byte[] { 2 }); // подписка на топик с паролем 

                    Password = txtReceived.Text;        // проверка о корректности пароля

                    pass_second_message = true;         // изменение pass_second_message

                    Pub.Visibility = Visibility.Visible;        // сделать видимым кнопку
                    Pass_Box.Visibility = Visibility.Visible;   // сделать видимым окно ввода пароля
                    Key_Label.Visibility = Visibility.Visible;  // сделать видимым label для расскладки клавиатуры


                }
                if (result == MessageBoxResult.No)      // если пользователь отказался
                {
                    client.Publish("Message_check", Encoding.UTF8.GetBytes("1"));   // публикация о закрытии 
                    client.Publish("Pass_check", Encoding.UTF8.GetBytes("True"));   // публикация топика об отказе 
                    timer.Start();                                                  // запуск таймера
                    txtReceived.Text = "false";                                     // обнуление txtReceived
                    Pub.Visibility = Visibility.Hidden;                             // скрытие кнопки публикации 
                    Pass_Box.Visibility = Visibility.Hidden;                        // скритие кнопки 
                    Key_Label.Visibility = Visibility.Hidden;                       // скрытие расскладки
                }
            }
        }
        // таймер для расскладки
        private void timerTick3(object sender, EventArgs e) 
        {
            switch (GetKeyboardLayout(0).ToInt64())
            {
                case 67699721:
                    Key_Label.Content = "En";
                    break;
                case 68748313:
                    Key_Label.Content = "Ru";
                    break;
                default:
                    Key_Label.Content = "Unknow";
                    break;

            }
        }

        private void Window_Loaded(object sender, RoutedEventArgs e)
        {

        }
        /*public void SetAutoload(bool set)
        {
            Microsoft.Win32.RegistryKey key = Microsoft.Win32.Registry.LocalMachine.OpenSubKey("SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run", true);
            if (set == true)
            {
                key.SetValue("Appname", "\"" + AppDomain.CurrentDomain.BaseDirectory + "Appname.exe" + "\"");
            }
            else
            {
                key.DeleteValue("WpfApp1", false);
            }
            key.Close();
        }*/
    }
}    
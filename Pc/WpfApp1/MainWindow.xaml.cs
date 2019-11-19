using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;


// including the M2Mqtt Library
using uPLibrary.Networking.M2Mqtt;
using uPLibrary.Networking.M2Mqtt.Messages;


namespace WpfApp1
{

    /// <summary>
    /// Логика взаимодействия для MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        MqttClient client;
        string clientId;
        string Password;

        public MainWindow()
        {
            InitializeComponent();

            //string BrokerAddress = "broker.hivemq.com";
            string BrokerAddress = "192.168.11.1";
            client = new MqttClient(BrokerAddress);

            // register a callback-function (we have to implement, see below) which is called by the library when a message was received
            client.MqttMsgPublishReceived += client_MqttMsgPublishReceived;

            // use a unique id as client id, each time we start the application
            clientId = Guid.NewGuid().ToString();
            client.Connect(clientId);
        }


        // this code runs when the main window closes (end of the app)
        protected override void OnClosed(EventArgs e)
        { 
            client.Disconnect();
            base.OnClosed(e);
            App.Current.Shutdown();
        }

        private void Button_Click(object sender, RoutedEventArgs e)
        {
            string Topic = "Accept";
            client.Subscribe(new string[] { Topic }, new byte[] { 2 });
            string check_Update = txtReceived.Text;

            if (check_Update == "true" || check_Update == "True")
            {
                Pub.Visibility = Visibility.Visible;
                Pass_Box.Visibility = Visibility.Visible;

                client.Unsubscribe(new string[] { Topic });
                Topic = "Pass_throw";

                client.Subscribe(new string[] { Topic }, new byte[] { 2 });
                Password = txtReceived.Text;
            }

            
        }

        // this code runs when a message was received

        private void Pub_Click(object sender, RoutedEventArgs e)
        {
            if (Pass_Box.Text == txtReceived.Text)
            {
                client.Publish("Pass_check", Encoding.UTF8.GetBytes("True"));
                Pass_Box.Text = "Should be fine";
            }

            //client.Publish("Exit_some_4", Encoding.UTF8.GetBytes(Convert.ToString(x)));
        }

        void client_MqttMsgPublishReceived(object sender, MqttMsgPublishEventArgs e)
        {
            string ReceivedMessage = Encoding.UTF8.GetString(e.Message);
            Dispatcher.Invoke(delegate { txtReceived.Text = ReceivedMessage; });            // we need this construction because the receiving code in the library and the UI with textbox run on different threads

        }
    }

}
    

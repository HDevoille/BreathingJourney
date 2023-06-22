import socket
from pylsl import StreamInlet, resolve_stream
import tkinter as tk
import threading

class GUI:

    def __init__(self):
        self.inlet = None 
        self.root = tk.Tk()
        
        self.root.geometry("500x300")
        self.root.title("Respiration")

        self.label = tk.Label(self.root,text = "Console :")
        self.label.pack(padx=20,pady=10)

        self.console = tk.Text(self.root,height=6)
        self.console.pack(padx=20,pady=10)

        self.buttonFindStream = tk.Button(self.root,text="Find Stream",command=threading.Thread(target=self.open_stream).start)
        self.buttonFindStream.pack(padx=20,pady=10)

        self.buttonTest = tk.Button(self.root, text="Test", command=threading.Thread(target=self.test).start)
        self.buttonTest.pack(padx=20,pady=10)

        self.buttonStart = tk.Button(self.root, text="Start Server", command = threading.Thread(target = self.start_server).start)
        self.buttonStart.pack(padx=20,pady=10)

        self.root.mainloop()

    def recv_data(self):
        sample,timestamp = self.inlet.pull_sample()
        return sample[0:4]

    def traitement_data(self):
        last_sample = self.recv_data()
        return last_sample
    
    def test(self):
        self.console.delete(1.0,tk.END)
        while True:
            message = str(self.compute_resp_rythm())
            self.console.insert(tk.END,message+"\n")
            self.console.see(tk.END)
            return message

    def compute_resp_rythm(self):
        resp_sample = []
        for n in range(10001):
            resp_sample.append(self.traitement_data()[1])
        cycle_count = 0
        for i in range(len(resp_sample)-10):
            if resp_sample[i] - resp_sample[i+10] == 0:
                cycle_count+=1
        return ((cycle_count/2)*6)/100

    def start_server(self):
        self.console.delete(1.0,tk.END)
        # Créer un socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Attacher le socket à une adresse et un port spécifiques
        server_socket.bind(('localhost', 12345))
        
        # Commencer à écouter pour les connexions entrantes
        server_socket.listen(1)
        self.console.insert(tk.END,"Server started and listening on localhost:12345 \n")

        while True:
            # Accepter une connexion entrante
            client_socket, addr = server_socket.accept()
            self.console.insert(tk.END,f"Connection from {addr} has been established! \n")

            while True:

                try:
                    # Envoyer un message au client
                    message = str(self.test())
                    client_socket.send(bytes(message+",", "utf-8"))
                    self.console.insert(tk.END,message+"\n")
                except:
                    self.console.insert(tk.END,"Client has disconnected \n")
                    break  # sortir de la boucle interne si le client est déconnecté

            # Fermer le socket client
            client_socket.close()

    def open_stream(self):
        self.console.delete(1.0,tk.END)
        self.console.insert(tk.END,"Looking for Stream ...")
        os_stream = resolve_stream("name","OpenSignals")
        self.inlet = StreamInlet(os_stream[0])
        self.console.insert(tk.END,"Stream found !")

if __name__ == "__main__":
    GUI()

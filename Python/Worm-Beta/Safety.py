from tkinter import *
import os
import shutil


def StartWorming():
    cd = os.getcwd()
    i = 1
    n = 0
    s = '-'

    while os.path.exists(f'{cd}/Worm {i}'):
        i += 1
        n += 1

    while i != n:
        os.mkdir(os.path.join(cd, f'Worm {i}'))
        os.chdir(f'{cd}/Worm {i}')

        with open(f'Worming{s}{i}.txt', 'w') as f:
            f.write('''COMPUTER WORM :-
                    A computer worm is a standalone malware computer program that replicates itself in order to spread to other computers. It often uses a computer network to spread itself, relying on security failures on the target computer to access it. It will use this machine as a host to scan and infect other computers. When these new worm-invaded computers are controlled, the worm will continue to scan and infect other computers using these computers as hosts, and this behaviour will continue. Computer worms use recursive methods to copy themselves without host programs and distribute themselves based on the law of exponential growth, thus controlling and infecting more and more computers in a short time. Worms almost always cause at least some harm to the network, even if only by consuming bandwidth, whereas viruses almost always corrupt or modify files on a targeted computer.Many worms are designed only to spread, and do not attempt to change the systems they pass through. However, as the Morris worm and Mydoom showed, even these "payload-free" worms can cause major disruption by increasing network traffic and other unintended effects.

        History:-
                 Morris worm source code floppy diskette at the Computer History Museum.
                 The actual term \"worm\" was first used in John Brunner\'s 1975 novel, The Shockwave Rider.
                 In the novel, Nichlas Haflinger designs and sets off a data-gathering worm in an act of revenge against the powerful men who run a national electronic information web that induces mass conformity.
                 \"You have the biggest-ever worm loose in the net, and it automatically sabotages any attempt to monitor it.
                 There\'s never been a worm with that tough a head or that long a tail!\".
                 The first ever computer worm was devised to be an anti-virus software.
                 Named Reaper, it was created by Ray Tomlinson to replicate itself across the ARPANET and delete the experimental Creeper program.
                 On November 2, 1988, Robert Tappan Morris, a Cornell University computer science graduate student, unleashed what became known as the Morris worm, disrupting many computers then on the Internet, guessed at the time to be one tenth of all those connected.
                 During the Morris appeal process, the U.S. Court of Appeals estimated the cost of removing the worm from each installation at between $200 and $53,000; this work prompted the formation of the CERT Coordination Center and Phage mailing list.
                 Morris himself became the first person tried and convicted under the 1986 Computer Fraud and Abuse Act.

        Features:-
                  1.Independence :-
                                   Computer viruses generally require a host program.
                                   The virus writes its own code into the host program.
                                   When the program runs, the written virus program is executed first, causing infection and damage.
                                   A worm does not need a host program, as it is an independent program or code chunk.
                                   Therefore, it is not restricted by the host program, but can run independently and actively carry out attacks.
                  2.Exploit attacks :-
                                      Because a worm is not limited by the host program, worms can take advantage of various operating system vulnerabilities to carry out active attacks.
                                      For example, the \"Nimda\" virus exploits vulnerabilities to attack.
                  3.Complexity :-
                                 Some worms are combined with web page scripts, and are hidden in HTML pages using VBScript, ActiveX and other technologies.
                                 When a user accesses a webpage containing a virus, the virus automatically resides in memory and waits to be triggered.
                                 There are also some worms that are combined with backdoor programs or Trojan horses, such as \"Code Red\".
                  4.Contagiousness :-
                                     Worms are more infectious than traditional viruses.
                                     They not only infect local computers, but also all servers and clients on the network based on the local computer.
                                     Worms can easily spread through shared folders, e-mails, malicious web pages, and servers with a large number of vulnerabilities in the network.
                  5.Harm :-
                           Any code designed to do more than spread the worm is typically referred to as the \"payload\".
                           Typical malicious payloads might delete files on a host system (e.g., the ExploreZip worm), encrypt files in a ransomware attack, or exfiltrate data such as confidential documents or passwords[citation needed].
                           Some worms may install a backdoor.
                           This allows the computer to be remotely controlled by the worm author as a \"zombie\".
                           Networks of such machines are often referred to as botnets and are very commonly used for a range of malicious purposes, including sending spam or performing DoS attacks.
                           Some special worms attack industrial systems in a targeted manner.
                           Stuxnet was primarily transmitted through LANs and infected thumb-drives, as its targets were never connected to untrusted networks, like the internet
                           This virus can destroy the core production control computer software used by chemical, power generation and power transmission companies in various countries around the world - in Stuxnet\'s case, Iran, Indonesia and India were hardest hit - it was used to \"issue orders\" to other equipment in the factory, and to hide those commands from being detected
                           Stuxnet used multiple vulnerabilities and four different zero-day exploits in Windows systems and Siemens SIMATICWinCC systems to attack the embedded programmable logic controllers of industrial machines.
                           Although these systems operate independently from the network, if the operator inserts a virus-infected disk into the system\'s USB interface, the virus will be able to gain control of the system without any other operational requirements or prompts.
                  6.Countermeasures :-
                                      Worms spread by exploiting vulnerabilities in operating systems.
                                      Vendors with security problems supply regular security updates (see \"Patch Tuesday\"), and if these are installed to a machine, then the majority of worms are unable to spread to it.
                                      If a vulnerability is disclosed before the security patch released by the vendor, a zero-day attack is possible.
                                      Users need to be wary of opening unexpected email, and should not run attached files or programs, or visit web sites that are linked to such emails.
                                      However, as with the ILOVEYOU worm, and with the increased growth and efficiency of phishing attacks, it remains possible to trick the end-user into running malicious code.
                                      Anti-virus and anti-spyware software are helpful, but must be kept up-to-date with new pattern files at least every few days.
                                      The use of a firewall is also recommended.
                                      Users can minimize the threat posed by worms by keeping their computers\' operating system and other software up to date, avoiding opening unrecognized or unexpected emails and running firewall and antivirus software.
        Mitigation techniques include :-
                                        ACLs in routers and switches
                                        Packet-filters
                                        TCP Wrapper/ACL enabled network service daemons
                                        Nullroute

        Infections can sometimes be detected by their behavior - typically scanning the Internet randomly, looking for vulnerable hosts to infect.
        In addition, machine learning techniques can be used to detect new worms, by analyzing the behavior of the suspected computer.

        Worms with good intent :-
                                 A helpful worm or anti-worm is a worm designed to do something that its author feels is helpful, though not necessarily with the permission of the executing computer\'s owner.
                                 Beginning with the first research into worms at Xerox PARC, there have been attempts to create useful worms.
                                 Those worms allowed John Shoch and Jon Hupp to test the Ethernet principles on their network of Xerox Alto computers[citation needed].
                                 Similarly, the Nachi family of worms tried to download and install patches from Microsoft\'s website to fix vulnerabilities in the host system by exploiting those same vulnerabilities.
                                 In practice, although this may have made these systems more secure, it generated considerable network traffic, rebooted the machine in the course of patching it, and did its work without the consent of the computer\'s owner or user.
                                 Regardless of their payload or their writers\' intentions, security experts regard all worms as malware.
                                 One study proposed the first computer worm that operates on the second layer of the OSI model (Data link Layer), utilizing topology information such as Content-addressable memory (CAM) tables and Spanning Tree information stored in switches to propagate and probe for vulnerable nodes until the enterprise network is covered.

                                 Anti-worms have been used to combat the effects of the Code Red, Blaster, and Santy worms.
                                 Welchia is an example of a helpful worm.
                                 Utilizing the same deficiencies exploited by the Blaster worm, Welchia infected computers and automatically began downloading Microsoft security updates for Windows without the users\' consent.
                                 Welchia automatically reboots the computers it infects after installing the updates.
                                 One of these updates was the patch that fixed the exploit.
                                 Other examples of helpful worms are \"Den_Zuko\", \"Cheeze\", \"CodeGreen\", and \"Millenium\".)\n\n''')

        os.chdir(cd)
        i += 1


def StopWorming():
    x = 1
    while not os.path.exists(f'{os.path.join(os.getcwd(), f"Worm {x}")}'):
        x += 1

    while os.path.exists(f'{os.path.join(os.getcwd(), f"Worm {x}")}'):
        shutil.rmtree(f'{os.path.join(os.getcwd(), f"Worm {x}")}')
        x += 1


def DelWorm():
    print(os.listdir(os.getcwd()))


class Worm:
    def __init__(self, root):
        self.root = root
        self.root.geometry('600x597+375+50')  # '600x597+200+50'
        self.root.title('Worm | Developed by Prathmesh')
        self.root.resizable(False, False)

        # ========Variables========
        self.executionPass = StringVar()
        self.terminationPass = StringVar()

        # ========Coloring Title========
        colTitle = Label(self.root, bg='black')
        colTitle.place(x=0, y=0, width=600, height=615)

        # ========Main Title========
        mainTitle = Label(self.root, text="Basic Worm", font=("times new roman", 40), bg='#053246', fg='white')
        mainTitle.place(x=0, y=0, relwidth=1)

        # ========Head Frame========
        headFrame = Frame(self.root, bd=4, relief=RIDGE, bg='black')
        headFrame.place(x=5, y=72, width=590, height=45)

        inpTitle = Label(headFrame, text='Operating Console', font=('goudy old style', 20), bg='#043256',
                         fg='white')
        inpTitle.place(x=0, y=0, relwidth=1)

        # ========Execution Frame========
        excFrame = Frame(self.root, bd=4, relief=RIDGE, bg='black')
        excFrame.place(x=5, y=72, width=590, height=45)

        txtExcTitle = Label(excFrame, text='Execution Password :-', font=('times new roman', 20), bg='black',
                            fg='white')
        txtExcTitle.place(x=3, y=3, width=270, height=30)

        txtExecPass = Entry(excFrame, font=('times new roman', 16, 'bold'), textvariable=self.executionPass,
                            bg='white')
        txtExecPass.place(x=286, y=3, relwidth=0.5, height=30)

        # ========Termination Frame========
        trmFrame = Frame(self.root, bd=4, relief=RIDGE, bg='black')
        trmFrame.place(x=5, y=122, width=590, height=45)

        txtTermTitle = Label(trmFrame, text='Deletion Password :-', font=('times new roman', 20), bg='black',
                             fg='white')
        txtTermTitle.place(x=9, y=3, width=240, height=30)

        txtTermPass = Entry(trmFrame, font=('times new roman', 16, 'bold'), textvariable=self.terminationPass,
                            bg='white')
        txtTermPass.place(x=286, y=3, relwidth=0.5, height=30)

        # ========Button Window========
        btnFrame = Frame(self.root, bd=4, relief=RIDGE, bg='black')
        btnFrame.place(x=5, y=172, width=590, height=50)

        btnExec = Button(btnFrame, text='Execute', command=StartWorming, font=('times new roman', 20, 'bold'),
                         bg='#2196f3', fg='black')
        btnExec.place(x=0, y=0, relwidth=0.4, relheight=1)

        btnStop = Button(btnFrame, text='Terminate', command=StopWorming, font=('times new roman', 20, 'bold'),
                         bg='#2196f3', fg='black')
        btnStop.place(x=233, y=0, relwidth=0.4, relheight=1)

        btnDel = Button(btnFrame, text='Delete', command=DelWorm, font=('times new roman', 20, 'bold'),
                        bg='#2196f3', fg='black')
        btnDel.place(x=466, y=0, relwidth=0.2, relheight=1)

        # ========Operation Frame========
        optFrame = Frame(self.root, bd=4, relief=RIDGE, bg='black')
        optFrame.place(x=5, y=227, width=590, height=365)

        optTitle = Label(optFrame, text='Operations', font=('goudy old style', 20), bg='#043256',
                         fg='white')
        optTitle.place(x=0, y=0, relwidth=1)

        # ========User Check Frame========
        uscFrame = Frame(self.root, bd=4, relief=RIDGE, bg='black')
        uscFrame.place(x=5, y=532, width=590, height=60)


root = Tk()
obj = Worm(root)
root.mainloop()

using System;
using System.Collections;
using System.Net.Sockets;
using System.Text;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using TMPro;

public class Spaceship_Movement : MonoBehaviour
{
    private TcpClient client;
    private NetworkStream stream;
    private Rigidbody2D rb;
    private float moveSpeed = 10f;
    public GameObject Text;
    public TMP_Text SpeedInfo;

    // Start is called before the first frame update
    void Start()
    {
        rb = GetComponent<Rigidbody2D>();
        client = new TcpClient("localhost", 12345);
        stream = client.GetStream();

        SpeedInfo = Text.GetComponent<TMP_Text>();
        SpeedInfo.text = "Speed : 0.0 Breathing rythm : 0.0";

        StartCoroutine(ReadMessages());
    }
    IEnumerator ReadMessages()
    {
        byte[] data = new byte[1024];

        while (true)
        {
            if (stream.DataAvailable)
            {
                int bytesRead = stream.Read(data, 0, data.Length);
                string message = Encoding.UTF8.GetString(data, 0, bytesRead);

                string[] val = message.Split(',');
                foreach (var number in val)
                {
                    Debug.Log(number);
                    float jump = try_float(number);
                    if(jump > 0.0)
                    {
                        float speed = jump * moveSpeed;
                        rb.velocity = new Vector2(speed,0f);
                        SpeedInfo.text = "Speed : " + speed.ToString() + " Breathing rythm : " + jump.ToString();
                    }
                }

                
            }

            yield return null;
        }
    }

    private float try_float(string v)
    {
        try
        {
            return float.Parse(v, System.Globalization.CultureInfo.InvariantCulture);
        } 
        catch
        {
            return 0.0f;
        }
        
    }

    void OnApplicationQuit()
    {
        client.Close();
    }

    // private Rigidbody2D rb;
    // private float DirX = 0f;
    // private float moveSpeed = 20f;
    // // Start is called before the first frame update
    // void Start()
    // {
    //     rb = GetComponent<Rigidbody2D>();
    // }

    // // Update is called once per frame
    // void Update()
    // {
    //     DirX = Input.GetAxis("Horizontal");
    //     rb.velocity = new Vector2(moveSpeed*DirX,0);
    // }
}

using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using System.IO;

public class MovimentaPe : MonoBehaviour
{
    //public Vector3 direcao;
    public GameObject Pe;
    public TextAsset csvFile;
    public float speed = 0.1f;
    private Rigidbody testePe;
    // Start is called before the first frame update
    // Update is called once per frame
 
    void Start ()
    {
        Time.timeScale = 1;
    }
    void Update ()
    {
        readCSV();
    }

    void readCSV()
    {
        string[] records = csvFile.text.Split('\n');
        for(int i = 1; i == records.Length; i++)
        {
            string[] fields = records[i].Split(',');
            transform.position = transform.position + new Vector3(float.Parse(fields[1])*Time.deltaTime*speed, float.Parse(fields[2])*Time.deltaTime*speed, float.Parse(fields[3])*Time.deltaTime*speed);
        }
    }
}
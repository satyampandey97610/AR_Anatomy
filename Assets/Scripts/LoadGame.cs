using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class LoadGame : MonoBehaviour {

	public void next(string a)
	{
		UnityEngine.SceneManagement.SceneManager.LoadScene(a);
	}
	
	public void QuitGame()
	{
		Debug.Log("Quti !");
		Application.Quit();
	}
}

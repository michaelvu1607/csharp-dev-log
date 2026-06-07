using UnityEngine;


public class ClearCounter : MonoBehaviour, IKitchenObjectParent
{
    [SerializeField] private KitchenObjectSO kitchenObjectSO;
    [SerializeField] private Transform kitchenObjectHoldPoint;

    private KitchenObject kitchenObject;
    public void Interact(Player player)
    {
        if (kitchenObject == null)
        {
            // duplicates item's prefab
            Transform kitchenObjectTransform = Instantiate(kitchenObjectSO.prefab, kitchenObjectHoldPoint);
            
            // passes this counter as the owner of the item
            // lets counter know it now owns the item
            kitchenObjectTransform.GetComponent<KitchenObject>().SetKitchenObjectParent(this);
            kitchenObjectTransform.localPosition = Vector3.zero;
        }
        else
        {
            // give item to player
            kitchenObject.SetKitchenObjectParent(player);
            
            //Debug.Log(kitchenObject.GetClearCounter());
        }
    }

    // public getter: provides socket
    public Transform GetKitchenObjectFollowTransform()
    {
        return kitchenObjectHoldPoint;
    }

    // public setter: item assignment in counter
    public void SetKitchenObject(KitchenObject kitchenObject)
    {
        this.kitchenObject = kitchenObject;
    }
    
    // checks which item the counter currently holds
    public KitchenObject GetKitchenObject()
    {
        return kitchenObject;
    }

    // clears counter
    public void ClearKitchenObject()
    {
        kitchenObject = null;
    }

    // helper function returning a boolean to check whether a counter is currently occupied
    public bool HasKitchenObject()
    {
        return kitchenObject != null;
    }
}

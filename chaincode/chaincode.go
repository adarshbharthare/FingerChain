package main

import (
    "encoding/json"
    "fmt"
    "github.com/hyperledger/fabric-contract-api-go/contractapi"
)

type SmartContract struct {
    contractapi.Contract
}

type Media struct {
    MediaID     string   `json:"mediaID"`
    OwnerID     string   `json:"ownerID"`
    Title       string   `json:"title"`
    Hash        string   `json:"hash"`
    Price       float64  `json:"price"`
    SaleStatus  string   `json:"saleStatus"`
    SharedUsers []string `json:"sharedUsers"`
}

type Owner struct {
    OwnerID string `json:"ownerID"`
    PKOwner string `json:"pkOwner"`
}

type User struct {
    UserID   string   `json:"userID"`
    PKUser   string   `json:"pkUser"`
    PurMedia []string `json:"purMedia"`
}

func (s *SmartContract) OwnerReg(ctx contractapi.TransactionContextInterface, ownerID, pkOwner string) error {
    owner := Owner{OwnerID: ownerID, PKOwner: pkOwner}
    ownerJSON, err := json.Marshal(owner)
    if err != nil {
        return err
    }
    return ctx.GetStub().PutState(ownerID, ownerJSON)
}

func (s *SmartContract) UserReg(ctx contractapi.TransactionContextInterface, userID, pkUser string) error {
    user := User{UserID: userID, PKUser: pkUser, PurMedia: []string{}}
    userJSON, err := json.Marshal(user)
    if err != nil {
        return err
    }
    return ctx.GetStub().PutState(userID, userJSON)
}

func (s *SmartContract) MediaUpload(ctx contractapi.TransactionContextInterface, mediaID, ownerID, title, hash string, price float64) error {
    media := Media{
        MediaID:     mediaID,
        OwnerID:     ownerID,
        Title:       title,
        Hash:        hash,
        Price:       price,
        SaleStatus:  "uploaded",
        SharedUsers: []string{},
    }
    mediaJSON, err := json.Marshal(media)
    if err != nil {
        return err
    }
    return ctx.GetStub().PutState(mediaID, mediaJSON)
}

func (s *SmartContract) MediaShare(ctx contractapi.TransactionContextInterface, mediaID, userID string) error {
    mediaBytes, err := ctx.GetStub().GetState(mediaID)
    if err != nil || mediaBytes == nil {
        return fmt.Errorf("media not found")
    }
    var media Media
    json.Unmarshal(mediaBytes, &media)
    media.SharedUsers = append(media.SharedUsers, userID)
    media.SaleStatus = "shared"
    mediaJSON, err := json.Marshal(media)
    if err != nil {
        return err
    }
    return ctx.GetStub().PutState(mediaID, mediaJSON)
}

func (s *SmartContract) MediaQuery(ctx contractapi.TransactionContextInterface, mediaID string) (string, error) {
    mediaBytes, err := ctx.GetStub().GetState(mediaID)
    if err != nil || mediaBytes == nil {
        return "", fmt.Errorf("media not found")
    }
    return string(mediaBytes), nil
}

func main() {
    chaincode, err := contractapi.NewChaincode(&SmartContract{})
    if err != nil {
        fmt.Printf("Error creating chaincode: %v\n", err)
    }
    if err := chaincode.Start(); err != nil {
        fmt.Printf("Error starting chaincode: %v\n", err)
    }
}


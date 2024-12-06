package main

import (
	"encoding/json"
	"github.com/PuerkitoBio/goquery"
	"log"
	"net/http"
	"os"
)

const url = "https://fsp-russia.com/region/regions/"

type Reg struct {
	Region  string `json:"region,omitempty"`
	Subject string `json:"subject,omitempty"`
	Person  string `json:"person,omitempty"`
	Email   string `json:"email,omitempty"`
}

func main() {
	res, err := http.Get(url)
	if err != nil {
		panic(err)
	}

	doc, err := goquery.NewDocumentFromReader(res.Body)
	if err != nil {
		log.Fatal(err)
	}

	var arr = []Reg{}
	doc.Find(".contacts_info > .contact_td").Each(func(i int, selection *goquery.Selection) {
		if i == 0 {
			return
		}

		subject := selection.Find(".cont.sub .white_region").Text()
		person := selection.Find(".cont.ruk .white_region").Text()
		email := selection.Find(".cont.con .white_region").Text()

		arr = append(arr, Reg{
			Region:  subject,
			Subject: subject,
			Person:  person,
			Email:   email,
		})
	})

	doc.Find(".accordion-item").Each(func(i int, selection *goquery.Selection) {
		region := selection.Find(".accordion-header h4").Text()
		selection.Find(".contact_td").Each(func(i int, selection *goquery.Selection) {
			subject := selection.Find(".cont.sub .white_region").Text()
			person := selection.Find(".cont.ruk .white_region").Text()
			email := selection.Find(".cont.con .white_region").Text()

			arr = append(arr, Reg{
				Region:  region,
				Subject: subject,
				Person:  person,
				Email:   email,
			})
		})
	})

	d, err := json.Marshal(arr)
	if err != nil {
		panic(err)
	}

	os.WriteFile("data.json", d, 0755)
}
